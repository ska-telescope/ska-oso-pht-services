"""
The schemas.sdp.sdp_configuration module defines Marshmallow schemas .
"""
from marshmallow import Schema, fields, post_load

from ska_oso_pdm.entities.sdp.sdp_configuration import SDPConfiguration

from .processing_block import ProcessingBlockSchema
from .scan_type import ScanTypeSchema

__all__ = ["SDPConfigurationSchema"]


class SDPConfigurationSchema(Schema):
    """
    Marshmallow class for the SDPConfiguration class
    """

    eb_id = fields.String(data_key="eb_id", required=True)
    max_length = fields.Float(data_key="max_length", required=True)
    scan_types = fields.Nested(ScanTypeSchema, many=True)
    processing_blocks = fields.Nested(ProcessingBlockSchema, many=True)

    @post_load
    def create_sdp_config(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a SDPConfiguration object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SDPConfiguration object populated from data
        """
        return SDPConfiguration(**data)
