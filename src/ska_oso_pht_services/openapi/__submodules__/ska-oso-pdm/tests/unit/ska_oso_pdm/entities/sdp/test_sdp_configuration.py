"""
Unit tests for the ska_oso_pdm.entities.sdp.sdp_configuration module.
"""

from ska_oso_pdm.entities.sdp import SDPConfiguration
from ska_oso_pdm.entities.sdp.processing_block import (
    PbDependency,
    ProcessingBlock,
    Workflow,
)
from ska_oso_pdm.entities.sdp.scan_type import Channel, ScanType


def test_sdp_configuration_equals():
    """
    Verify that SDPConfiguration objects are considered equal
    """
    channel = Channel(
        744, 0, 2, 0.35e9, 0.368e9, [(0, 0), (200, 1), (744, 2), (944, 3)]
    )
    scan_type1 = ScanType("science_A", "123", [channel])
    scan_type2 = ScanType("calibration_B", "123", [channel])

    wf1 = Workflow("vis_receive", "realtime", "0.1.0")
    wf2 = Workflow("test_realtime", "realtime", "0.1.0")
    wf3 = Workflow("ical", "batch", "0.1.0")
    wf4 = Workflow("dpreb", "batch", "0.1.0")

    dep1 = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])
    dep2 = PbDependency("pb-mvp01-20200325-00003", ["calibration"])

    pb1 = ProcessingBlock("pb-mvp01-20200325-00001", wf1, {})
    pb2 = ProcessingBlock("pb-mvp01-20200325-00002", wf2, {})
    pb3 = ProcessingBlock("pb-mvp01-20200325-00003", wf3, {}, [dep1])
    pb4 = ProcessingBlock("pb-mvp01-20200325-00004", wf4, {}, [dep2])

    sdp1 = SDPConfiguration(
        "sbi-mvp01-20200325-00001",
        100.0,
        [scan_type1, scan_type2],
        [pb1, pb2, pb3, pb4],
    )
    sdp2 = SDPConfiguration(
        "sbi-mvp01-20200325-00001",
        100.0,
        [scan_type1, scan_type2],
        [pb1, pb2, pb3, pb4],
    )

    assert sdp1 == sdp2

    assert sdp1 != SDPConfiguration(
        "sbi-mvp01-20200325-00001", 0.0, [scan_type1, scan_type2], [pb1, pb2, pb3, pb4]
    )
    assert sdp1 != SDPConfiguration(
        "sbi-mvp01-20200325-00001", 100.0, None, [pb1, pb2, pb3, pb4]
    )
    assert sdp1 != SDPConfiguration(
        "sbi-mvp01-20200325-00002", 100.0, [scan_type1, scan_type2], None
    )
    assert sdp1 != SDPConfiguration(None, None, None, None)


def test_sdp_configuration_not_equal_to_other_objects():
    """
    Verify that SDPConfiguration objects are not considered equal to objects of
    other types.
    """
    sdp = SDPConfiguration(None, None, None, None)
    assert sdp != 1
