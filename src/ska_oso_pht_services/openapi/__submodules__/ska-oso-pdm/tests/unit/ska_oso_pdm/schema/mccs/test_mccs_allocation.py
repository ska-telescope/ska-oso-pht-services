"""
tests for the mccs_allocation to validate the
conversion between the JSON and Python representations
of an SKA Scheduling Block
"""

from ska_oso_pdm.entities.mccs.mccs_allocation import MCCSAllocation
from ska_oso_pdm.schemas.mccs.mccs_allocation import MCCSAllocationSchema
from tests.unit.ska_oso_pdm.utils import assert_json_is_equal

VALID_OBJECT = MCCSAllocation(
    station_ids=[[1, 2], [3, 4]],
    channel_blocks=[3, 4],
    subarray_beam_ids=["Beam A", "Beam B"],
)

VALID_JSON = """
{
    "station_ids": [[1, 2], [3, 4]],
    "channel_blocks": [3, 4],
    "subarray_beam_ids": ["Beam A", "Beam B"]
}
"""


def test_marshal():
    """
    Verify that MCCSAllocation is marshaled to JSON correctly.
    """
    marshaled = MCCSAllocationSchema().dumps(VALID_OBJECT)
    assert_json_is_equal(marshaled, VALID_JSON)


def test_unmarshal():
    """
    Verify that JSON is unmarshaled to an MCCSAllocation correctly.
    """
    unmarshaled = MCCSAllocationSchema().loads(VALID_JSON)
    assert unmarshaled == VALID_OBJECT
