"""
The schemas.sdp.processing_block module defines Marshmallow schemas .
"""
from marshmallow import Schema, fields, post_dump, post_load

from ska_oso_pdm.entities.sdp import PbDependency, ProcessingBlock, Workflow

__all__ = ["WorkflowSchema", "PbDependencySchema", "ProcessingBlockSchema"]


class WorkflowSchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Represents the type of workflow being configured on the SDP
    """

    name = fields.String(data_key="name", required=True)
    kind = fields.String(data_key="kind", required=True)
    version = fields.String(data_key="version", required=True)

    @post_load
    def create_sdp_wf(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a Workflow object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDP Workflow object populated from data
        """
        name = data["name"]
        kind = data["kind"]
        version = data["version"]
        return Workflow(name, kind, version)


class PbDependencySchema(Schema):  # pylint: disable=too-few-public-methods
    """
    Marshmallow schema for the PbDepedency class.
    """

    pb_id = fields.String(data_key="pb_id")
    kind = fields.List(fields.String, data_key="kind")

    @post_load
    def create_pb_dependency(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a PbDependency object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: PbDependency object populated from data
        """
        pb_id = data["pb_id"]
        kind = data["kind"]
        return PbDependency(pb_id, kind)


class ProcessingBlockSchema(Schema):
    """
    Marshmallow schema for the ProcessingBlock class.
    """

    pb_id = fields.String(data_key="pb_id", required=True)
    workflow = fields.Nested(WorkflowSchema)
    parameters = fields.Dict()
    dependencies = fields.Nested(PbDependencySchema, many=True, missing=None)

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for PB configuration
        """
        return {k: v for k, v in data.items() if v is not None}

    @post_load
    def create_processing_block(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a PB object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: PB object populated from data
        """
        return ProcessingBlock(**data)
