import json
import logging
import os
from typing import Any, Dict, Optional, cast

import boto3
import botocore

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


class ClusterRunningError(Exception):
    pass


def parse_bool(v: str) -> bool:
    return str(v).lower() in ("yes", "true", "t", "1")


def handler(event: Dict[str, Any], context: Optional[Dict[str, Any]]) -> Dict[str, Any]:

    try:
        logger.info(f"Lambda metadata: {json.dumps(event)} (type = {type(event)})")
        default_fail_if_cluster_running = parse_bool(event.get("DefaultFailIfClusterRunning", False))

        # This will work for {"JobInput": {"FailIfClusterRunning": true}} or {"FailIfClusterRunning": true}
        fail_if_cluster_running = parse_bool(
            event.get("ExecutionInput", event).get("FailIfClusterRunning", default_fail_if_cluster_running)
        )

        # check if job flow already exists
        if fail_if_cluster_running:
            cluster_name = event.get("Input", {}).get("Name", "")
            cluster_is_running = False
            logger.info(f'Checking if job flow "{cluster_name}" is running already')
            response = emr.list_clusters(ClusterStates=["STARTING", "BOOTSTRAPPING", "RUNNING", "WAITING"])
            for job_flow_running in response["Clusters"]:
                jf_name = job_flow_running["Name"]
                cluster_id = job_flow_running["Id"]
                if jf_name == cluster_name:
                    logger.info(f"Job flow {cluster_name} is already running: terminate? {fail_if_cluster_running}")
                    cluster_is_running = True
                    break

            if cluster_is_running and fail_if_cluster_running:
                raise ClusterRunningError(
                    f"Found running Cluster with name {cluster_name}. "
                    f"ClusterId: {cluster_id}. FailIfClusterRunning is {fail_if_cluster_running}"
                )
            else:
                return cast(Dict[str, Any], event["Input"])

        else:
            return cast(Dict[str, Any], event["Input"])

    except Exception as e:
        logger.error(f"Error processing event {json.dumps(event)}")
        logger.exception(e)
        raise e
