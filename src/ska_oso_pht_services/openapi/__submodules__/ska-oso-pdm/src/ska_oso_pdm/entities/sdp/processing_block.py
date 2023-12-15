"""
The entities.sdp.processing_block module defines a Python representation of
a processing block for SDP configuration.
"""

from typing import Dict, List

__all__ = ["Workflow", "ProcessingBlock", "PbDependency"]

ProcessingBlockID = str


class Workflow:  # pylint: disable=too-few-public-methods
    """
    Class to hold Workflow for ProcessingBlock
    """

    def __init__(self, name: str, kind: str, version: str):
        self.name = name
        self.kind = kind
        self.version = version

    def __eq__(self, other):
        if not isinstance(other, Workflow):
            return False
        return (
            self.name == other.name
            and self.kind == other.kind
            and self.version == other.version
        )

    def __repr__(self):
        return (
            f"<ProcessingBlock("
            f"name={self.name}, "
            f"kind={self.kind}, "
            f"version={self.version})>"
        )


class PbDependency:
    """
    Class to hold Dependencies for ProcessingBlock
    """

    def __init__(self, pb_id: ProcessingBlockID, kind: List[str]):
        self.pb_id = pb_id
        self.kind = kind

    def __eq__(self, other):
        if not isinstance(other, PbDependency):
            return False
        return self.pb_id == other.pb_id and self.kind == other.kind

    def __repr__(self):
        return f"<ProcessingBlock(" f"pb_id={self.pb_id}, " f"kind={self.kind})>"


class ProcessingBlock:
    """
    Class to hold ProcessingBlock configuration
    """

    def __init__(
        self,
        pb_id: ProcessingBlockID,
        workflow: Workflow,
        parameters: Dict,
        dependencies: List[PbDependency] = None,
    ):
        self.pb_id = pb_id
        self.workflow = workflow
        self.parameters = parameters
        self.dependencies = dependencies

    def __eq__(self, other):
        if not isinstance(other, ProcessingBlock):
            return False
        return (
            self.pb_id == other.pb_id
            and self.workflow == other.workflow
            and self.parameters == other.parameters
            and self.dependencies == other.dependencies
        )

    def __repr__(self):
        return (
            f"<ProcessingBlock("
            f"pb_id={self.pb_id}, "
            f"workflow={self.workflow}, "
            f"parameters={self.parameters}, "
            f"dependencies={self.dependencies})>"
        )
