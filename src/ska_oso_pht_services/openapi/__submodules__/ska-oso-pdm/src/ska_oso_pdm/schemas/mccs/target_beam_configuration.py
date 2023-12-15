"""
The schemas.target_beam_configuration defines a Marshmallow schema that maps
SKA LOW subarray beams, target  to/from a JSON representation.
"""
from marshmallow import Schema, fields, post_load

from ska_oso_pdm.entities.mccs.target_beam_configuration import TargetBeamConfiguration
from ska_oso_pdm.schemas import CODEC

__all__ = ["TargetBeamConfigurationSchema"]


@CODEC.register_mapping(TargetBeamConfiguration)
class TargetBeamConfigurationSchema(Schema):
    """
    The Target beam configuration schema section of an SKA scheduling block
    """

    target_beam_id = fields.String(required=True, data_key="target_beam_id")
    target = fields.String(required=True, data_key="target")
    subarray_beam_configuration = fields.String(
        required=True, data_key="subarray_beam_configuration"
    )

    @post_load
    def create_target_beam(self, data, **_):  # pylint: disable=no-self-use
        """
        Convert parsed JSON back into a TargetBeamConfiguration

        :param data: dict containing parsed JSON values
        :param _: kwargs passed by Marshmallow
        :return: TargetBeamConfiguration instance populated to match JSON
        """
        target_beam_id = data["target_beam_id"]
        target = data["target"]
        subarray_beam_config = data["subarray_beam_configuration"]
        return TargetBeamConfiguration(
            target_beam_id=target_beam_id,
            target=target,
            subarray_beam_configuration=subarray_beam_config,
        )
