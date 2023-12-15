"""
Unit tests for the ska_oso_pdm.entities.dish_allocation module.
"""

from ska_oso_pdm.entities.dish.dish_allocation import DishAllocation


def test_dish_allocation_repr():
    """
    Verify that the DishAllocation repr is formatted correctly.
    """
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    assert repr(dish_allocation) == "<DishAllocation(receptor_ids=['ac', 'b', 'aab'])>"


def test_dish_allocation_eq():
    """
    Verify that two DishAllocations with the same allocated receptors are
    considered equal.
    """
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    assert dish_allocation == DishAllocation(receptor_ids=["ac", "b", "aab"])
    assert dish_allocation == DishAllocation(receptor_ids=["b", "ac", "aab"])
    assert dish_allocation != DishAllocation(receptor_ids=["ac"])
    assert dish_allocation != DishAllocation(receptor_ids=["ac", "b", "aab", "d"])


def test_dish_allocation_eq_with_other_objects():
    """
    Verify that a DishAllocation is considered unequal to objects of other
    types.
    """
    dish_allocation = DishAllocation(receptor_ids=["ac", "b", "aab"])
    assert dish_allocation != 1
    assert dish_allocation != object()
