"""
tests for the processing_block schema to validate the
conversion between the JSON and Python representations
of the processing block section of an SDP configuration
"""
from ska_oso_pdm.entities.sdp.processing_block import (
    PbDependency,
    ProcessingBlock,
    Workflow,
)
from ska_oso_pdm.schemas.sdp.processing_block import (
    PbDependencySchema,
    ProcessingBlockSchema,
    WorkflowSchema,
)
from tests.unit.ska_oso_pdm.utils import assert_json_is_equal

VALID_PROCESSING_BLOCK_JSON = """
{
  "pb_id": "pb-mvp01-20200325-00003",
  "workflow": {"kind": "batch", "name": "ical", "version": "0.1.0"},
  "parameters": {},
  "dependencies": [
    {"pb_id": "pb-mvp01-20200325-00001", "kind": ["visibilities"]}
  ]
}"""
VALID_PROCESSING_BLOCK_NO_DEP_JSON = """
{
  "pb_id": "pb-mvp01-20200325-00003",
  "workflow": {"kind": "batch", "name": "ical", "version": "0.1.0"},
  "parameters": {}
}"""
VALID_PROCESSING_BLOCK_DEPENDENCY_JSON = """
{
  "pb_id": "pb-mvp01-20200325-00001",
  "kind": ["visibilities"]
}
"""
VALID_WORKFLOW_JSON = '{"kind": "batch", "name": "ical", "version": "0.1.0"}'


def test_marshall_processing_block():

    """
    Verify that ProcessingBlockSchema is marshalled to JSON correctly.
    """
    workflow = Workflow("ical", "batch", "0.1.0")
    dep = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])

    request = ProcessingBlock("pb-mvp01-20200325-00003", workflow, {}, [dep])
    json_str = ProcessingBlockSchema().dumps(request)
    assert_json_is_equal(json_str, VALID_PROCESSING_BLOCK_JSON)


def test_unmarshall_processing_block():
    """
    Verify that JSON can be unmarshalled back to a ProcessingBlock object
    """
    workflow = Workflow("ical", "batch", "0.1.0")
    dep = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])

    expected = ProcessingBlock("pb-mvp01-20200325-00003", workflow, {}, [dep])

    schema = ProcessingBlockSchema()
    result = schema.loads(VALID_PROCESSING_BLOCK_JSON)

    assert result == expected


def test_marshall_processing_block_without_dependencies():

    """
    Verify that ProcessingBlock is marshalled to JSON correctly when no
    dependencies are defined.
    """
    workflow = Workflow("ical", "batch", "0.1.0")

    # SDP Processing block
    request = ProcessingBlock("pb-mvp01-20200325-00003", workflow, {})
    json_str = ProcessingBlockSchema().dumps(request)
    assert_json_is_equal(json_str, VALID_PROCESSING_BLOCK_NO_DEP_JSON)


def test_unmarshall_processing_block_without_dependencies():
    """
    Verify that JSON can be unmarshalled back to a ProcessingBlock object when
    no dependencies are defined.
    """
    workflow = Workflow("ical", "batch", "0.1.0")

    expected = ProcessingBlock("pb-mvp01-20200325-00003", workflow, {})

    schema = ProcessingBlockSchema()
    result = schema.loads(VALID_PROCESSING_BLOCK_NO_DEP_JSON)

    assert result == expected


def test_marshall_workflow():
    """
    Verify that Workflow is marshalled to JSON correctly.
    """
    request = Workflow("ical", "batch", "0.1.0")

    json_str = WorkflowSchema().dumps(request)
    assert_json_is_equal(json_str, VALID_WORKFLOW_JSON)


def test_unmarshall_workflow():
    """
    Verify that JSON can be unmarshalled back to a Workflow object
    """
    expected = Workflow("ical", "batch", "0.1.0")

    schema = WorkflowSchema()
    result = schema.loads(VALID_WORKFLOW_JSON)

    assert result == expected


def test_marshal_processing_block_dependency():

    """
    Verify that PbDependency is marshalled to JSON correctly.
    """
    request = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])

    json_str = PbDependencySchema().dumps(request)
    assert_json_is_equal(json_str, VALID_PROCESSING_BLOCK_DEPENDENCY_JSON)


def test_unmarshall_processing_block_dependency():
    """
    Verify that JSON can be unmarshalled back to a PbDependency object
    """
    expected = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])

    schema = PbDependencySchema()
    result = schema.loads(VALID_PROCESSING_BLOCK_DEPENDENCY_JSON)

    assert result == expected
