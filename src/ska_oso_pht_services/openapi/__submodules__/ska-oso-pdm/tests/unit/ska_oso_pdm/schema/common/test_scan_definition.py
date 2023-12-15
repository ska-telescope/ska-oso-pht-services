"""
tests for the scan_definitions_schema to validate the
conversion between the JSON and Python representations
of the scan definitions section of an SKA Scheduling Block
"""

from datetime import timedelta

from ska_oso_pdm.entities.common.scan_definition import ScanDefinition
from ska_oso_pdm.schemas.common.scan_definition import ScanDefinitionSchema
from tests.unit.ska_oso_pdm.utils import assert_json_is_equal

schema = ScanDefinitionSchema()

VALID_SKAMID_SCANDEFINITION = ScanDefinition(
    scan_definition_id="id_42",
    scan_duration=timedelta(hours=1.0),
    scan_type_id="science",
    dish_configuration_id="dish config 123",
    target_id="m51",
    csp_configuration_id="csp_id_41",
)

VALID_SKAMID_SCANDEFINITION_JSON = """
{
    "scan_definition_id": "id_42",
    "scan_duration": 3600000,
    "target": "m51",
    "csp_configuration": "csp_id_41",
    "dish_configuration": "dish config 123",
    "scan_type": "science"
}
"""

VALID_SKALOW_SCANDEFINITION = ScanDefinition(
    scan_definition_id="id_43",
    scan_duration=timedelta(seconds=12.3),
    target_beam_configuration_ids=["beam 1", "beam 2"],
    target_id="drift scan",
)

VALID_SKALOW_SCANDEFINITION_JSON = """
{
    "scan_definition_id": "id_43",
    "scan_duration": 12300,
    "target_beam_configurations": ["beam 1", "beam 2"],
    "target": "drift scan"
}
"""

VALID_SCANDEFINITION_WITHOUT_OPTIONAL_PARAMS = ScanDefinition(
    scan_definition_id="id_42", scan_duration=timedelta(minutes=30)
)

VALID_SCANDEFINITION_WITHOUT_OPTIONAL_PARAMS_JSON = """
{
    "scan_definition_id": "id_42",
    "scan_duration": 1800000
}
"""


def test_marshall_scan_definition_mid():
    """
    Verify that ScanDefinition is marshalled to JSON correctly for an
    SKA MID scan definition
    """

    result = schema.dumps(VALID_SKAMID_SCANDEFINITION)

    assert_json_is_equal(result, VALID_SKAMID_SCANDEFINITION_JSON)


def test_marshall_scan_definition_low():
    """
    Verify that ScanDefinition is marshalled to JSON correctly for an
    SKA LOW scan definition
    """

    result = schema.dumps(VALID_SKALOW_SCANDEFINITION)

    assert_json_is_equal(result, VALID_SKALOW_SCANDEFINITION_JSON)


def test_marshall_scan_definition_without_optional_parameters():
    """
    Verify that ScanDefinition is marshalled to JSON correctly
    when optional ScanDefinition parameters are not included.
    """
    result = schema.dumps(VALID_SCANDEFINITION_WITHOUT_OPTIONAL_PARAMS)

    assert_json_is_equal(result, VALID_SCANDEFINITION_WITHOUT_OPTIONAL_PARAMS_JSON)


def test_unmarshall_scan_definition():
    """
    Verify that JSON can be unmarshalled back to a ScanDefinition
    """

    result = schema.loads(VALID_SKAMID_SCANDEFINITION_JSON)
    assert result == VALID_SKAMID_SCANDEFINITION


def test_unmarshall_scan_definition_without_optional_parameters():
    """
    Verify that JSON can be unmarshalled back to a ScanDefinition
    when CSPConfiguration is not included in JSON
    """
    result = schema.loads(VALID_SCANDEFINITION_WITHOUT_OPTIONAL_PARAMS_JSON)

    assert result == VALID_SCANDEFINITION_WITHOUT_OPTIONAL_PARAMS


def test_unmarshall_lowscandefinition():
    """
    Verify that JSON can be unmarshalled back to a LowScanDefinition
    """
    result = schema.loads(VALID_SKALOW_SCANDEFINITION_JSON)
    assert result == VALID_SKALOW_SCANDEFINITION
