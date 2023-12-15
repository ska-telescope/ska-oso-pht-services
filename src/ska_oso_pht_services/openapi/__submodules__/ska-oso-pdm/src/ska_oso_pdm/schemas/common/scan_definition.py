"""
The schemas.scan_definition_schema defines a Marshmallow schema that maps
The scan definition section of an SKA scheduling block  to/from a JSON representation.
"""
from marshmallow import Schema, fields, post_dump, post_load

from ska_oso_pdm.entities.common.scan_definition import ScanDefinition

__all__ = ["ScanDefinitionSchema"]


class ScanDefinitionSchema(Schema):
    """
    The scan definition section of an SKA scheduling block
    """

    scan_definition_id = fields.String(required=True)
    scan_duration = fields.TimeDelta(
        precision=fields.TimeDelta.MILLISECONDS, required=True
    )
    target_beam_configuration_ids = fields.List(
        fields.Str(), data_key="target_beam_configurations"
    )
    dish_configuration_id = fields.String(data_key="dish_configuration")
    scan_type_id = fields.String(data_key="scan_type")
    csp_configuration_id = fields.String(data_key="csp_configuration")
    target_id = fields.String(data_key="target")

    @post_load
    def create_scan_definition(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a ScanDefinition

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: ScanDefinitions instance populated to match JSON
        """
        # Note: The ScanDefinition constructor arguments have the
        # same name as the data keys, so we can pass in **data directly
        return ScanDefinition(**data)

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for scan definition
        """
        return {k: v for k, v in data.items() if v is not None}
