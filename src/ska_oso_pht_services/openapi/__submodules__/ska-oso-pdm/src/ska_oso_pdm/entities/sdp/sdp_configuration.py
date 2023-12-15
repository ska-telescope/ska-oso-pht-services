"""
The ska_oso_pdm.entities.common.sdp.sdp_configuration module defines a Python
object model for the SDP configuration JSON string passed to
CentralNode.AssignResources.
"""

from typing import List

from .processing_block import ProcessingBlock
from .scan_type import ScanType

__all__ = ["SDPConfiguration"]


class SDPConfiguration:
    """
    SDPConfiguration captures the SDP resources and pipeline configuration
    required to process an execution block.
    """

    def __init__(
        self,
        eb_id: str,
        max_length: float,
        scan_types: List[ScanType],
        processing_blocks: List[ProcessingBlock],
    ):
        """
        Create a new SDPConfiguration.

        :param eb_id: execution block ID
        :param max_length: maximum length
        :param scan_types: list of SDP scan types
        :param processing_blocks: list of SDP ProcessingBlock objects
        """
        self.eb_id = eb_id
        self.max_length = max_length
        self.scan_types = scan_types
        self.processing_blocks = processing_blocks

    def __eq__(self, other):
        if not isinstance(other, SDPConfiguration):
            return False
        return (
            self.eb_id == other.eb_id
            and self.max_length == other.max_length
            and self.scan_types == other.scan_types
            and self.processing_blocks == other.processing_blocks
        )

    def __repr__(self):
        return (
            f"<SDPConfiguration(id={self.eb_id}, "
            f"max_length={self.max_length}, "
            f"scan_types={self.scan_types}, "
            f"processing_blocks={self.processing_blocks})>"
        )
