"""
Unit tests for the ska_oso_pdm.entities.sdp.processing_block module.
"""

from ska_oso_pdm.entities.sdp.processing_block import (
    PbDependency,
    ProcessingBlock,
    Workflow,
)


def test_workflow_equals():
    """
    Verify that Workflow objects are considered equal when they have:
     - the same ID
     - the same type
     - the same version
    """
    workflow1 = Workflow("name", "kind", "version")
    workflow2 = Workflow("name", "kind", "version")
    assert workflow1 == workflow2

    assert workflow1 != Workflow("", "kind", "version")
    assert workflow1 != Workflow("name", "", "version")
    assert workflow1 != Workflow("name", "kind", "")


def test_workflow_not_equal_to_other_objects():
    """
    Verify that Workflow objects are not considered equal to objects of
    other types.
    """
    workflow = Workflow("name", "kind", "version")
    assert workflow != 1


def test_pb_dependency_equals():
    """
    Verify that PBDependency objects are considered equal when they have:
     - the same PB ID
     - the same type
    """
    dep1 = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])
    dep2 = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])

    assert dep1 == dep2

    assert dep1 != PbDependency("pb-mvp01-20200325-00001", ["calibration"])
    assert dep1 != PbDependency("pb-mvp01-20200325-00003", ["calibration"])


def test_pb_dependency_not_equal_to_other_objects():
    """
    Verify that PBDependency objects are not considered equal to objects of
    other types.
    """
    dep = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])
    assert dep != 1


def test_processing_block_equals():
    """
    Verify that ProcessingBlock objects are considered equal
    """
    w_flow = Workflow("vis_receive", "realtime", "0.1.0")
    dep = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])
    pb1 = ProcessingBlock("pb-mvp01-20200325-00003", w_flow, {}, [dep])
    pb2 = ProcessingBlock("pb-mvp01-20200325-00003", w_flow, {}, [dep])

    assert pb1 == pb2

    assert pb1 != ProcessingBlock("pb-mvp01-20200325-00001", w_flow, {}, [dep])
    assert pb1 != ProcessingBlock("pb-mvp01-20200325-00001", None, {}, [dep])
    assert pb1 != ProcessingBlock("pb-mvp01-20200325-00003", w_flow, None, [dep])
    assert pb1 != ProcessingBlock("pb-mvp01-20200325-00003", w_flow, {})


def test_processing_block_not_equal_to_other_objects():
    """
    Verify that ProcessingBlock objects are not considered equal to objects of
    other types.
    """
    p_block = ProcessingBlock("pb-mvp01-20200325-00003", None, None, None)
    assert p_block != 1
