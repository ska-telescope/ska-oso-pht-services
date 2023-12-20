"""
The schemas.subarray_beam_configuration defines a Marshmallow schema that maps
SKA LOW subarray beams, target  to/from a JSON representation.
"""
from marshmallow import Schema, fields, post_load

from ska_oso_pdm.entities.mccs.subarray_beam_configuration import (
    SubarrayBeamConfiguration,
)
from ska_oso_pdm.schemas import CODEC

__all__ = ["SubarrayBeamConfigurationSchema"]


@CODEC.register_mapping(SubarrayBeamConfiguration)
class SubarrayBeamConfigurationSchema(Schema):
    """
    The MCCS subarray beam configuration schema section of an SKA scheduling
    block.
    """

    subarray_beam_configuration_id = fields.String(required=True)
    subarray_beam_id = fields.String(required=True)
    update_rate = fields.Float(required=True)
    antenna_weights = fields.List(fields.Float(), required=True)
    phase_centre = fields.List(fields.Float(), required=True)
    channels = fields.List(fields.List(fields.Integer), required=True)

    @post_load
    def create_subarray_beam(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a SubarrayBeamConfiguration

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: SubarrayBeamConfiguration instance populated to match JSON
        """
        subarray_beam_configuration_id = data["subarray_beam_configuration_id"]
        subarray_beam_id = data["subarray_beam_id"]
        update_rate = data["update_rate"]
        antenna_weights = data["antenna_weights"]
        phase_centre = data["phase_centre"]
        channels = data["channels"]

        return SubarrayBeamConfiguration(
            subarray_beam_configuration_id=subarray_beam_configuration_id,
            subarray_beam_id=subarray_beam_id,
            update_rate=update_rate,
            antenna_weights=antenna_weights,
            phase_centre=phase_centre,
            channels=channels,
        )
