"""
Unit tests for the ska_oso_pdm.entities.mccs_allocation module.
"""
from ska_oso_pdm.entities.mccs.mccs_allocation import MCCSAllocation

BEAM_ID_A = "Beam A"
BEAM_ID_B = "Beam B"


def test_mccs_allocate_eq():
    """
    Verify that two MCCSAllocation objects with the same allocated elements are
    considered equal.
    """

    mccs_allocate = MCCSAllocation(
        station_ids=[[1, 2], [3, 4]],
        channel_blocks=[3, 4],
        subarray_beam_ids=[BEAM_ID_A, BEAM_ID_B],
    )
    assert mccs_allocate == MCCSAllocation(
        station_ids=[[1, 2], [3, 4]],
        channel_blocks=[3, 4],
        subarray_beam_ids=[BEAM_ID_A, BEAM_ID_B],
    )

    assert mccs_allocate != MCCSAllocation(
        station_ids=[[1, 2], [3, 4]],
        channel_blocks=[3, 5],
        subarray_beam_ids=[BEAM_ID_A, BEAM_ID_B],
    )
    assert mccs_allocate != MCCSAllocation(
        station_ids=[[1, 2], [3, 4]],
        channel_blocks=[3, 4],
        subarray_beam_ids=[BEAM_ID_A, "Beam C"],
    )


def test_mccs_allocate_eq_with_other_objects():
    """
    Verify that a MCCSAllocation is considered unequal to objects of other
    types.
    """
    mccs_allocate = MCCSAllocation(
        station_ids=[[1, 2], [3, 4]],
        channel_blocks=[3, 4],
        subarray_beam_ids=[BEAM_ID_A, BEAM_ID_B],
    )
    assert mccs_allocate != 1
    assert mccs_allocate != object()
