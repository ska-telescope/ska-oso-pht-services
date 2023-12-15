"""
Unit tests for the ska_oso_pdm.entities.target_beam_configuration module.
"""

from ska_oso_pdm.entities.mccs.target_beam_configuration import TargetBeamConfiguration


def test_target_beam_configuration_eq():
    """
    Verify that TargetBeamConfiguration objects are considered equal when:
      - they use the same subarray beam and target
    """

    config_1 = TargetBeamConfiguration(
        "science target beam", "my science target", "subarray beam 1"
    )
    config_2 = TargetBeamConfiguration(
        "science target beam", "my science target", "subarray beam 1"
    )
    config_3 = TargetBeamConfiguration(
        "science target beam", "my science target", "subarray beam 2"
    )
    config_4 = TargetBeamConfiguration(
        "science target beam", "my science target 1", "subarray beam 2"
    )
    config_5 = TargetBeamConfiguration(
        "science target beam2", "my science target 2", "subarray beam 2"
    )

    assert config_1 == config_2
    assert config_1 != config_3
    assert config_1 != config_4
    assert config_1 != config_5


def test_target_beam_configuration_is_not_equal_to_other_objects():
    """
    Verify that TargetBeamConfiguration is considered unequal to
    non-TargetBeamConfiguration objects.
    :return:
    """
    config_1 = TargetBeamConfiguration(
        "science target beam", "my science target", "subarray beam 1"
    )
    assert config_1 != object
