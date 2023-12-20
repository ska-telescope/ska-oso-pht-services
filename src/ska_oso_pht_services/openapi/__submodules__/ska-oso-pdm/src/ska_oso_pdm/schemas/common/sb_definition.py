"""
The schemas.scheduling_block_schema defines a Marshmallow schema that maps
the scan definition section of an SKA scheduling block  to/from a JSON representation.
"""
from marshmallow import Schema, fields, post_dump, post_load
from marshmallow_enum import EnumField

from ska_oso_pdm.entities.common.sb_definition import (
    MetaData,
    SBDefinition,
    TelescopeType,
)
from ska_oso_pdm.schemas import CODEC
from ska_oso_pdm.schemas.common.procedures import PythonProcedureSchema
from ska_oso_pdm.schemas.common.scan_definition import ScanDefinitionSchema
from ska_oso_pdm.schemas.common.target import TargetSchema
from ska_oso_pdm.schemas.csp.common import CSPConfigurationSchema
from ska_oso_pdm.schemas.dish.dish_allocation import DishAllocationSchema
from ska_oso_pdm.schemas.dish.dish_configuration import DishConfigurationSchema
from ska_oso_pdm.schemas.mccs.mccs_allocation import MCCSAllocationSchema
from ska_oso_pdm.schemas.mccs.subarray_beam_configuration import (
    SubarrayBeamConfigurationSchema,
)
from ska_oso_pdm.schemas.mccs.target_beam_configuration import (
    TargetBeamConfigurationSchema,
)
from ska_oso_pdm.schemas.sdp import SDPConfigurationSchema

__all__ = ["MetaDataSchema", "SBDefinitionSchema"]


class MetaDataSchema(Schema):
    """
    The MetaData section of an SKA scheduling block
    """

    version = fields.Integer(required=True)
    created_on = fields.DateTime(format="iso", required=True)
    created_by = fields.String(required=True, allow_none=True)
    last_modified_on = fields.DateTime(format="iso", allow_none=True)
    last_modified_by = fields.String(allow_none=True)

    @post_load
    def create_metadata(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a metadata

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SBDefinition instance populated to match JSON
        """
        return MetaData(**data)

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for metadata
        """
        return {k: v for k, v in data.items() if v is not None}


@CODEC.register_mapping(SBDefinition)
class SBDefinitionSchema(Schema):
    """
    SKA scheduling block
    """

    sbd_id = fields.String(required=True, data_key="sbd_id")

    interface = fields.String(required=True)

    telescope = EnumField(
        TelescopeType,
        dump_by=EnumField.VALUE,
        load_by=EnumField.VALUE,
        required=True,
        error="{input} not a valid TelescopeType. Must be one of: {values}",
    )

    metadata = fields.Nested(MetaDataSchema, required=True)

    activities = fields.Dict(fields.String(), fields.Nested(PythonProcedureSchema))

    scan_definitions = fields.List(
        fields.Nested(ScanDefinitionSchema),
    )

    scan_sequence = fields.List(fields.Str())

    sdp_configuration = fields.Nested(
        SDPConfigurationSchema,
        data_key="sdp_configuration",
        allow_none=True,  # temporary until sdp details for LOW are known
    )

    csp_configurations = fields.List(
        fields.Nested(CSPConfigurationSchema),
        allow_none=True,  # temporary until csp details for LOW are known
    )

    dish_configurations = fields.Nested(DishConfigurationSchema, many=True)

    dish_allocations = fields.Nested(DishAllocationSchema, allow_none=True)

    mccs_allocation = fields.Nested(MCCSAllocationSchema, allow_none=True)

    subarray_beam_configurations = fields.Nested(
        SubarrayBeamConfigurationSchema,
        many=True,
        allow_none=True,
    )

    target_beam_configurations = fields.Nested(
        TargetBeamConfigurationSchema,
        many=True,
        allow_none=True,
    )

    targets = fields.Nested(TargetSchema, many=True, allow_none=True)

    @post_load
    def create_scheduling_block(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a ScanRequest

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SBDefinition instance populated to match JSON
        """
        return SBDefinition(**data)

    SKIP_VALUES = [None, []]

    @post_dump
    def filter_nulls(self, data, **_):  # pylint: disable=no-self-use
        """
        Filter out null values from JSON.

        :param data: Marshmallow-provided dict containing parsed object values
        :param _: kwargs passed by Marshmallow
        :return: dict suitable for scan definition
        """
        return {k: v for k, v in data.items() if v not in self.SKIP_VALUES}
