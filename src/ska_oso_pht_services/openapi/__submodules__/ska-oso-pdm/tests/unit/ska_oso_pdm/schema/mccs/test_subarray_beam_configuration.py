"""
tests for the subarray_beam_configuration to validate the
conversion between the JSON and Python representations
of an SKA Scheduling Block
"""

from ska_oso_pdm.entities.mccs.subarray_beam_configuration import (
    SubarrayBeamConfiguration,
)
from ska_oso_pdm.schemas.mccs.subarray_beam_configuration import (
    SubarrayBeamConfigurationSchema,
)
from tests.unit.ska_oso_pdm.utils import assert_json_is_equal

VALID_REQUEST = """
{
      "subarray_beam_configuration_id": "beam config 1",
      "subarray_beam_id": "subarray beam A",
      "update_rate": 0.0,
      "antenna_weights": [1.0, 1.0, 1.0],
      "phase_centre": [0.0, 0.0],
      "channels": [
        [0, 8, 1, 1],
        [8, 8, 2, 1],
        [24, 16, 2, 1]
      ]
}
"""

VALID_OBJECT = SubarrayBeamConfiguration(
    subarray_beam_configuration_id="beam config 1",
    subarray_beam_id="subarray beam A",
    update_rate=0.0,
    antenna_weights=[1.0, 1.0, 1.0],
    phase_centre=[0.0, 0.0],
    channels=[[0, 8, 1, 1], [8, 8, 2, 1], [24, 16, 2, 1]],
)


def test_marshal():
    """
    Verify that SubarrayBeamConfiguration is marshaled to JSON correctly.
    """
    marshaled = SubarrayBeamConfigurationSchema().dumps(VALID_OBJECT)
    assert_json_is_equal(marshaled, VALID_REQUEST)


def test_unmarshal():
    """
    Verify that JSON can be unmarshaled back to an SubarrayBeamConfiguration
    object.
    """
    unmarshaled = SubarrayBeamConfigurationSchema().loads(VALID_REQUEST)
    assert unmarshaled == VALID_OBJECT
