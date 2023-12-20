"""
The entities module provides simple Python representations of the structured
request and response for the TMC CentralNode.AssignResources command.
"""
from typing import List

__all__ = ["MCCSAllocation", "SubarrayBeamID"]

# MCCS subarray beam ID that will be mapped to an integer at runtime
SubarrayBeamID = str


class MCCSAllocation:
    """
    MCCSAllocation is a Python representation of the MCCS allocation segment
    of a scheduling block.
    """

    def __init__(
        self,
        station_ids: List[List[int]],
        channel_blocks: List[int],
        subarray_beam_ids: List[SubarrayBeamID],
    ):
        """
        Create a new Subarray object.

        :param station_ids: stations id's to allocate
        :param channel_blocks: number of channel groups to assign
        :param subarray_beam_ids: beam IDs
        """
        self.station_ids = station_ids
        self.channel_blocks = channel_blocks
        self.subarray_beam_ids = subarray_beam_ids

    def __eq__(self, other):
        """
        Check for equality between two allocate objects

        :param other: the object to check against this allocate object
        :type other: allocate object

        :return: returns True if the objects are the same, else False
        :rtype: boolean
        """
        if not isinstance(other, MCCSAllocation):
            return False
        return (
            self.station_ids == other.station_ids
            and self.channel_blocks == other.channel_blocks
            and self.subarray_beam_ids == other.subarray_beam_ids
        )

    def __repr__(self):
        return (
            f"<MCCSAllocation("
            f"station_ids={self.station_ids}, "
            f"channel_blocks={self.channel_blocks}, "
            f"subarray_beam_ids={self.subarray_beam_ids})>"
        )
