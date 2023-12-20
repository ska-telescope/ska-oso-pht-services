"""
tests for the dish_allocation_schema to validate the
conversion between the JSON and Python representations
of an SKA Scheduling Block
"""
from ska_oso_pdm.entities.dish.dish_allocation import DishAllocation
from ska_oso_pdm.schemas.dish.dish_allocation import DishAllocationSchema
from tests.unit.ska_oso_pdm.utils import assert_json_is_equal

VALID_DISH_ALLOCATION_JSON = '{"receptor_ids": ["0001", "0002"]}'


def test_marshall_dish_allocation_to_json():
    """
    Verify that DishAllocation is marshalled to JSON correctly.
    """
    config = DishAllocation(receptor_ids=["0001", "0002"])
    json_str = DishAllocationSchema().dumps(config)
    assert_json_is_equal(json_str, VALID_DISH_ALLOCATION_JSON)


def test_unmarshall_dish_allocation_from_json():
    """
    Verify that JSON can be unmarshalled to a DishAllocation
    """

    expected = DishAllocation(receptor_ids=["0001", "0002"])
    unmarshalled = DishAllocationSchema().loads(VALID_DISH_ALLOCATION_JSON)
    assert unmarshalled == expected
