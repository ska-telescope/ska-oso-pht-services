"""
tests for the target_beam_configuration to validate the
conversion between the JSON and Python representations
of an SKA Scheduling Block
"""

from ska_oso_pdm.entities.mccs.target_beam_configuration import TargetBeamConfiguration
from ska_oso_pdm.schemas.mccs.target_beam_configuration import (
    TargetBeamConfigurationSchema,
)
from tests.unit.ska_oso_pdm.utils import assert_json_is_equal

VALID_TARGET_BEAM_CONFIG_REQUEST = """
{
    "target_beam_id": "science target beam",
    "target": "my science target",
    "subarray_beam_configuration": "subarray beam 1"
}
"""


def test_marshal_target_beam_configuration():
    """
    Verify that TargetBeamConfiguration is marshalled to JSON correctly.
    """
    request = TargetBeamConfiguration(
        "science target beam", "my science target", "subarray beam 1"
    )

    json_str = TargetBeamConfigurationSchema().dumps(request)
    assert_json_is_equal(json_str, VALID_TARGET_BEAM_CONFIG_REQUEST)


def test_unmarshall_mccs_allocate_resources():
    """
    Verify that JSON can be unmarshalled back to an TargetBeamConfiguration
    object.
    """
    expected = TargetBeamConfiguration(
        "science target beam", "my science target", "subarray beam 1"
    )
    request = TargetBeamConfigurationSchema().loads(VALID_TARGET_BEAM_CONFIG_REQUEST)
    assert request == expected
