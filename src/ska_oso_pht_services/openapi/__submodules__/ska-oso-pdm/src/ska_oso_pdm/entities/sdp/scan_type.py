"""
The entities.sdp.scan_type module defines a Python representation of
a scan type for SDP configuration.
"""

from typing import List, Tuple

from ska_oso_pdm.entities.common.target import TargetID

__all__ = ["ScanType", "ScanTypeID", "Channel"]

ScanTypeID = str


class Channel:
    """
    Class to hold Channels for ScanType
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        count: int,
        start: int,
        stride: int,
        freq_min: float,
        freq_max: float,
        link_map: List[Tuple],
    ):
        self.count = count
        self.start = start
        self.stride = stride
        self.freq_min = freq_min
        self.freq_max = freq_max
        self.link_map = link_map

    def __eq__(self, other):
        if not isinstance(other, Channel):
            return False
        return (
            self.count == other.count
            and self.start == other.start
            and self.stride == other.stride
            and self.freq_min == other.freq_min
            and self.freq_max == other.freq_max
            and self.link_map == other.link_map
        )

    def __repr__(self):
        return (
            f"<Channel (count={self.count}, start={self.start}, "
            f"stride={self.stride}, "
            f"freq_min={self.freq_min}, freq_max={self.freq_max}, "
            f"link_map={self.link_map})>"
        )


class ScanType:
    """
    Class to hold ScanType configuration
    """

    def __init__(
        self, scan_type_id: ScanTypeID, target_id: TargetID, channels: List[Channel]
    ):
        self.scan_type_id = scan_type_id
        self.target_id = target_id
        self.channels = channels

    def __eq__(self, other):
        if not isinstance(other, ScanType):
            return False
        return (
            self.scan_type_id == other.scan_type_id
            and self.target_id == other.target_id
            and self.channels == other.channels
        )

    def __repr__(self):
        return (
            f"<ScanType(id={self.scan_type_id}, "
            f"target_id={self.target_id}, "
            f"channels={self.channels})>"
        )
