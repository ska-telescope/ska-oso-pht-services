"""
The schemas.mccs_allocation module defines Marshmallow schemas that map TMC
Central Node message classes to/from a JSON representation.
"""
from marshmallow import Schema, fields, post_load

from ska_oso_pdm.entities.mccs.mccs_allocation import MCCSAllocation
from ska_oso_pdm.schemas import CODEC

__all__ = ["MCCSAllocationSchema"]


@CODEC.register_mapping(MCCSAllocation)
class MCCSAllocationSchema(Schema):
    """
    Marshmallow schema for the MCCSAllocation class.
    """

    station_ids = fields.List(fields.List(fields.Integer), required=True)
    channel_blocks = fields.List(fields.Integer, required=True)
    subarray_beam_ids = fields.List(fields.Str, required=True)

    @post_load
    def create_mccs_allocate(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a MCCSAllocation object.

        :param data: Marshmallow-provided dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow

        :return: MCCSAllocation object populated from data
        """
        station_ids = data["station_ids"]
        channel_blocks = data["channel_blocks"]
        subarray_beam_ids = data["subarray_beam_ids"]
        return MCCSAllocation(
            station_ids=station_ids,
            channel_blocks=channel_blocks,
            subarray_beam_ids=subarray_beam_ids,
        )
