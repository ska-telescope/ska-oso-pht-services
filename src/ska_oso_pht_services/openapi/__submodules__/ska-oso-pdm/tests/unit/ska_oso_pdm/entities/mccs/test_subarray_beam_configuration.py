"""
Unit tests for the ska_oso_pdm.entities.subarray_beam_configuration module.
"""

from ska_oso_pdm.entities.mccs.subarray_beam_configuration import (
    SubarrayBeamConfiguration,
)

CONSTRUCTOR_ARGS = dict(
    subarray_beam_configuration_id="beam config 1",
    subarray_beam_id="subarray beam A",
    update_rate=0.0,
    antenna_weights=[1.0, 1.0, 1.0],
    phase_centre=[0.0, 0.0],
    channels=[[0, 8, 1, 1], [8, 8, 2, 1], [24, 16, 2, 1]],
)


def test_subarray_beam_configuration_eq():
    """
    Verify that SubarrayBeamConfiguration objects are considered equal when:
      - they use the same subarray beam and target
    """
    obj = SubarrayBeamConfiguration(**CONSTRUCTOR_ARGS)
    assert obj == SubarrayBeamConfiguration(**CONSTRUCTOR_ARGS)

    alt_constructor_args = dict(
        subarray_beam_configuration_id="beam config 2",
        subarray_beam_id="subarray beam B",
        update_rate=0.1,
        antenna_weights=[1.0, 1.0, 0.0],
        phase_centre=[0.0, 1.0],
        channels=[[0, 8, 1, 1], [8, 8, 2, 1], [24, 16, 2, 3]],
    )

    for key, value in alt_constructor_args.items():
        alt_args = dict(CONSTRUCTOR_ARGS)
        alt_args[key] = value
        other = SubarrayBeamConfiguration(**alt_args)
        assert obj != other


def test_subarray_beam_configuration_is_not_equal_to_other_objects():
    """
    Verify that SubarrayBeamConfiguration is considered unequal to
    non-SubarrayBeamConfiguration objects.
    :return:
    """
    obj = SubarrayBeamConfiguration(**CONSTRUCTOR_ARGS)
    assert obj != object()
