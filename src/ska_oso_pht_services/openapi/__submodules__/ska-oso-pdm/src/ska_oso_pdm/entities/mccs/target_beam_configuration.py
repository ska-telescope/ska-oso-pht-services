"""
The entities.target_beam_configuration module defines
simple Python representation of how SKA Low subarray beam
in sub-array should be configured.
"""
from ska_oso_pdm.entities.common.target import TargetID

from .subarray_beam_configuration import SubarrayBeamConfigurationID

__all__ = ["TargetBeamConfiguration", "TargetBeamConfigurationID"]

TargetBeamConfigurationID = str


class TargetBeamConfiguration:  # pylint: disable=too-few-public-methods
    """
    TargetBeamConfiguration specifies how SKA LOW subarray beam in a sub-array should be
    configured.
    """

    def __init__(
        self,
        target_beam_id: TargetBeamConfigurationID,
        target: TargetID,
        subarray_beam_configuration: SubarrayBeamConfigurationID,
    ):
        """
        Create a new TargetBeamConfiguration.

        :param target_beam_id: ID of target beam configuration
        :param target: target beam configuration points at this target
        :param subarray_beam_configuration: sub-array beam configuration
        """
        self.target_beam_id = target_beam_id
        self.target = target
        self.subarray_beam_configuration = subarray_beam_configuration

    def __eq__(self, other):
        if not isinstance(other, TargetBeamConfiguration):
            return False
        return (
            self.target_beam_id == other.target_beam_id
            and self.target == other.target
            and self.subarray_beam_configuration == other.subarray_beam_configuration
        )

    def __repr__(self):
        return (
            f"<TargetBeamConfiguration("
            f"target_beam_id={self.target_beam_id}, "
            f"target={self.target}, "
            f"subarray_beam_configuration={self.subarray_beam_configuration})>"
        )
