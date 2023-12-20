"""
The entities.subarray_beam_configuration module defines
simple Python representation of how SKA Low subarray beam
in sub-array should be configured.
"""
__all__ = ["SubarrayBeamConfiguration", "SubarrayBeamConfigurationID"]

from typing import List

from .mccs_allocation import SubarrayBeamID

SubarrayBeamConfigurationID = str


class SubarrayBeamConfiguration:  # pylint: disable=too-few-public-methods
    """
    SubarrayBeamConfiguration specifies how SKA LOW sub-array should be
    configured.
    """

    def __init__(
        self,
        subarray_beam_configuration_id: SubarrayBeamConfigurationID,
        subarray_beam_id: SubarrayBeamID,
        update_rate: float,
        antenna_weights: List[float],
        phase_centre: List[float],
        channels: List[List[int]],
    ):  # pylint: disable=too-many-arguments
        """
        Create a new SubarrayBeamConfiguration.

        :param subarray_beam_configuration_id: ID for this configuration
        :param subarray_beam_id: ID of subarray beam this config maps to
        :param update_rate: rate of updates (in units of ???)
        :param antenna_weights:
        :param phase_centre:
        :param channels:
        """
        self.subarray_beam_configuration_id = subarray_beam_configuration_id
        self.subarray_beam_id = subarray_beam_id
        self.update_rate = update_rate
        self.antenna_weights = antenna_weights
        self.phase_centre = phase_centre
        self.channels = channels

    def __eq__(self, other):
        if not isinstance(other, SubarrayBeamConfiguration):
            return False
        return (
            self.subarray_beam_configuration_id == other.subarray_beam_configuration_id
            and self.subarray_beam_id == other.subarray_beam_id
            and self.update_rate == other.update_rate
            and self.antenna_weights == other.antenna_weights
            and self.phase_centre == other.phase_centre
            and self.channels == other.channels
        )

    def __repr__(self):
        return (
            f"<SubarrayBeamConfiguration("
            f"subarray_beam_configuration_id={self.subarray_beam_configuration_id}, "
            f"subarray_beam_id={self.subarray_beam_id}, "
            f"update_rate={self.update_rate}, "
            f"antenna_weights={self.antenna_weights}, "
            f"phase_centre={self.phase_centre}, "
            f"channels={self.channels})>"
        )
