import base64
import json
import logging
import os
from datetime import date, datetime
from typing import Any, Dict, List, Optional

import boto3
import botocore
from botocore.exceptions import ClientError

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def _get_botocore_config() -> botocore.config.Config:
    product = os.environ.get("AWS_EMR_LAUNCH_PRODUCT", "")
    version = os.environ.get("AWS_EMR_LAUNCH_VERSION", "")
    return botocore.config.Config(
        retries={"max_attempts": 5},
        connect_timeout=10,
        max_pool_connections=10,
        user_agent_extra=f"{product}/{version}",
    )


def _boto3_client(service_name: str) -> boto3.client:
    return boto3.Session().client(service_name=service_name, use_ssl=True, config=_get_botocore_config())


emr = _boto3_client("emr")
sfn = _boto3_client("stepfunctions")
events = _boto3_client("events")
secretsmanager = _boto3_client("secretsmanager")


class SecretNotFoundError(Exception):
    pass


class SecretDecryptionFailureError(Exception):
    pass


def json_serial(obj: object) -> str:
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def get_secret_value(secret_id: str) -> Dict[str, Any]:
    try:
        secret_response = secretsmanager.get_secret_value(SecretId=secret_id)
    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            raise SecretDecryptionFailureError(f"SecretDecryptionFailure: {secret_id}")
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            raise SecretNotFoundError(f"SecretNotFound: {secret_id}")
        else:
            raise e

    val: Dict[str, Any] = (
        json.loads(secret_response.pop("SecretString"))
        if "SecretString" in secret_response
        else json.loads(base64.b64decode(secret_response.pop("SecretBinary")))
    )
    logger.info(f"SecretFound: {secret_id}")
    return val


def log_and_raise(e: Exception, event: Dict[str, Any]) -> None:
    logger.error(f"Error processing event {json.dumps(event)}")
    logger.exception(e)
    raise e


def update_configurations(
    configurations: List[Dict[str, Any]], classification: str, properties: Dict[str, str]
) -> List[Dict[str, Any]]:
    found_classification = False
    for config in configurations:
        cls = config.get("Classification", "")
        if cls == classification:
            found_classification = True
            config["Properties"] = dict(config.get("Properties", {}), **properties)

    if not found_classification:
        configurations.append({"Classification": classification, "Properties": properties})

    return configurations


def handler(event: Dict[str, Any], context: Optional[Dict[str, Any]]) -> None:
    try:
        logger.info(f"Lambda metadata: {json.dumps(event)} (type = {type(event)})")
        cluster_configuration = event["Input"]["Cluster"]
        task_token = event.get("TaskToken", None)
        cluster_status_lambda = event.get("CheckStatusLambda", None)
        fire_and_forget = event.get("FireAndForget", False)
        secret_configurations = event["Input"].get("SecretConfigurations", None)
        kerberos_attributes_secret = event["Input"].get("KerberosAttributesSecret", None)
        rule_name = event.get("RuleName", None)

        # NoneType values need to be removed from the cluster_configuration
        logger.info(f"Preparing ClusterConfiguration: {json.dumps(cluster_configuration)}")
        cluster_configuration = {k: v for k, v in cluster_configuration.items() if v is not None}
        cluster_configuration["Instances"] = {
            k: v for k, v in cluster_configuration["Instances"].items() if v is not None
        }
        logger.info(f"Removed NoneType values from ClusterConfiguration: {json.dumps(cluster_configuration)}")

        if secret_configurations:
            logger.info(f"Getting SecretConfigurations: {json.dumps(secret_configurations)}")
            for classification, secret_id in secret_configurations.items():
                properties = get_secret_value(secret_id)
                cluster_configuration["Configurations"] = update_configurations(
                    cluster_configuration["Configurations"], classification, properties
                )

        if kerberos_attributes_secret:
            logger.info(f"Getting KerberosAttributesSecret: {json.dumps(kerberos_attributes_secret)}")
            kerberos_attributes = get_secret_value(kerberos_attributes_secret)
            cluster_configuration["KerberosAttributes"] = {
                k: v
                for k, v in kerberos_attributes.items()
                if k
                in [
                    "Realm",
                    "KdcAdminPassword",
                    "ADDomainJoinUser",
                    "ADDomainJoinPassword",
                    "CrossRealmTrustPrincipalPassword",
                ]
            }

        logger.info("Calling RunJobFlow")
        response = emr.run_job_flow(**cluster_configuration)

        logger.info(f"Got JobFlow response {json.dumps(response)}")
        cluster_id = response["JobFlowId"]

        if fire_and_forget:
            response["ClusterId"] = cluster_id
            logger.info(
                f"Sending Task Success, TaskToken: {task_token}, "
                f"Output: {json.dumps(response, default=json_serial)}"
            )
            sfn.send_task_success(taskToken=task_token, output=json.dumps(response, default=json_serial))
        else:
            target_input = {
                "Id": cluster_id,
                "Arn": cluster_status_lambda,
                "Input": json.dumps(
                    {
                        "ClusterId": cluster_id,
                        "TaskToken": task_token,
                        "RuleName": rule_name,
                        "ExpectedState": "WAITING",
                    }
                ),
            }
            logger.info(f"Putting Rule Targets: {json.dumps(target_input)}")
            failed_targets = events.put_targets(Rule=rule_name, Targets=[target_input])
            if failed_targets["FailedEntryCount"] > 0:
                failed_entries = failed_targets["FailedEntries"]
                raise Exception(f"Failed Putting Targets: {json.dumps(failed_entries)}")

            logger.info(f"Enabling Rule: {rule_name}")
            events.enable_rule(Name=rule_name)
    except Exception as e:
        log_and_raise(e, event)
