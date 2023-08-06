#!/usr/bin/env python3

import os

import aws_cdk
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_sns as sns
from aws_cdk import aws_stepfunctions as sfn

from aws_emr_launch.constructs.emr_constructs import emr_code
from aws_emr_launch.constructs.step_functions import emr_chains, emr_tasks

NAMING_PREFIX = f"emr-launch-{aws_cdk.Aws.ACCOUNT_ID}-{aws_cdk.Aws.REGION}"

app = aws_cdk.App()
stack = aws_cdk.Stack(
    app,
    "PersistentPipelineStack",
    env=aws_cdk.Environment(account=os.environ["CDK_DEFAULT_ACCOUNT"], region=os.environ["CDK_DEFAULT_REGION"]),
)

# SNS Topics for Success/Failures messages from our Pipeline
success_topic = sns.Topic(stack, "SuccessTopic")
failure_topic = sns.Topic(stack, "FailureTopic")

# The bucket to deploy Step artifacts to
artifacts_bucket = s3.Bucket.from_bucket_name(stack, "ArtifactsBucket", f"{NAMING_PREFIX}-artifacts")

# Prepare the scripts executed by our Steps for deployment
# This uses the Artifacts bucket defined in Cluster Configuration used by our
# Launch Function
step_code = emr_code.Code.from_path(
    path="./step_sources", deployment_bucket=artifacts_bucket, deployment_prefix="persistent_pipeline/step_sources"
)

# Create a Chain to receive Failure messages
fail = emr_chains.Fail(
    stack,
    "FailChain",
    message=sfn.TaskInput.from_json_path_at("$.Error"),
    subject="Pipeline Failure",
    topic=failure_topic,
)

# Create a Parallel Task for the Phase 1 Steps
phase_1 = sfn.Parallel(stack, "Phase1", result_path="$.Result.Phase1")

# Add a Failure catch to our Parallel phase
phase_1.add_catch(fail, errors=["States.ALL"], result_path="$.Error")

# Create 5 Phase 1 Parallel Steps. The number of concurrently running Steps is
# defined in the Cluster Configuration
for file in emr_code.Code.files_in_path("./step_sources", "test_step_*.sh"):
    # Define an AddStep Task for Each Step
    step_task = emr_tasks.AddStepBuilder.build(
        stack,
        f"Phase1_{file}",
        emr_step=emr_code.EMRStep(
            name=f"Phase 1 - {file}",
            jar="s3://us-west-2.elasticmapreduce/libs/script-runner/script-runner.jar",
            args=[f"{step_code.s3_path}/{file}", "Arg1", "Arg2"],
            code=step_code,
        ),
        cluster_id=sfn.TaskInput.from_json_path_at("$.ClusterId").value,
    )
    phase_1.branch(step_task)


# Create a Parallel Task for the Phase 2 Steps
phase_2 = sfn.Parallel(stack, "Phase2", result_path="$.Result.Phase2")

# Add a Failure catch to our Parallel phase
phase_2.add_catch(fail, errors=["States.ALL"], result_path="$.Error")

# Create 5 Phase 2 Parallel Hive SQL Steps.
for file in emr_code.Code.files_in_path("./step_sources", "test_step_*.hql"):
    # Define an AddStep Task for Each Step
    step_task = emr_tasks.AddStepBuilder.build(
        stack,
        f"Phase2_{file}",
        emr_step=emr_code.EMRStep(
            name=f"Phase 2 - {file}",
            jar="command-runner.jar",
            args=[
                "hive-script",
                "--run-hive-script",
                "--args",
                "-f",
                f"{step_code.s3_path}/{file}",
                "-d" "ARG1=Arg1",
                "-d",
                "ARG2=Arg2",
            ],
            code=step_code,
        ),
        cluster_id=sfn.TaskInput.from_json_path_at("$.ClusterId").value,
    )
    phase_2.branch(step_task)

# A Chain for Success notification when the pipeline completes
success = emr_chains.Success(
    stack,
    "SuccessChain",
    message=sfn.TaskInput.from_json_path_at("$.Result"),
    subject="Pipeline Succeeded",
    topic=success_topic,
)

# Assemble the Pipeline
definition = sfn.Chain.start(phase_1).next(phase_2).next(success)

state_machine = sfn.StateMachine(
    stack, "PersistentPipeline", state_machine_name="persistent-multi-phase-pipeline", definition=definition
)

app.synth()
