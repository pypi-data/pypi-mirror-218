import os

import aws_cdk
from logzero import logger

import constructs
from aws_emr_launch import __product__, __version__


def _tag_construct(construct: constructs.Construct) -> None:
    suppress_tags = os.environ.get("SUPPRESS_EMR_LAUNCH_DEPLOYMENT_TAGS", "").lower() in ("1", "t", "true", "y", "yes")

    if not suppress_tags:
        aws_cdk.Tags.of(construct).add("deployment:product:name", __product__)
        aws_cdk.Tags.of(construct).add("deployment:product:version", __version__)
    else:
        logger.info('Suppressing "deployment:product" tags for: %s', construct.node.id)


class BaseConstruct(constructs.Construct):
    def __init__(self, scope: constructs.Construct, id: str):
        super().__init__(scope, id)
        _tag_construct(self)


class BaseBuilder:
    @staticmethod
    def tag_construct(construct: constructs.Construct) -> None:
        _tag_construct(construct)
