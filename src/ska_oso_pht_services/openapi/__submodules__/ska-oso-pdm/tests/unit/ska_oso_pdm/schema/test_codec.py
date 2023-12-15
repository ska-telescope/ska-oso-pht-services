"""
Unit tests for the ska_oso_pdm.schemas.codec module.
"""
import os.path

import pytest

from ska_oso_pdm.entities.common.sb_definition import SBDefinition
from ska_oso_pdm.schemas import CODEC
from tests.unit.ska_oso_pdm.schema.common import test_sb_definition
from tests.unit.ska_oso_pdm.utils import assert_json_is_equal


def test_mid_codec_loads():
    """
    Verify that the codec unmarshalls objects correctly.
    """
    unmarshalled = CODEC.loads(
        SBDefinition, test_sb_definition.VALID_MID_SBDEFINITION_JSON
    )
    expected = test_sb_definition.create_test_mid_sbdefinition()
    assert expected == unmarshalled


def test_mid_codec_dumps():
    """
    Verify that the codec marshalls objects to JSON.
    """
    expected = test_sb_definition.VALID_MID_SBDEFINITION_JSON
    obj = test_sb_definition.create_test_mid_sbdefinition()
    marshalled = CODEC.dumps(obj)

    assert_json_is_equal(marshalled, expected)


def test_read_a_mid_file_from_disk():
    """
    Test for loading an SBDefinition from a JSON file
    """
    cwd, _ = os.path.split(__file__)
    test_data = os.path.join(cwd, "common/testfile_sample_mid_sb.json")
    result = CODEC.load_from_file(SBDefinition, test_data)
    expected = test_sb_definition.create_test_mid_sbdefinition()
    assert result == expected


def test_low_codec_loads():
    """
    Verify that the codec unmarshalls objects correctly._
    """
    unmarshalled = CODEC.loads(
        SBDefinition, test_sb_definition.VALID_LOW_SBDEFINITION_JSON
    )
    expected = test_sb_definition.create_test_low_sbdefinition()
    assert expected == unmarshalled


def test_low_codec_dumps():
    """
    Verify that the codec marshalls objects to JSON.
    """
    expected = test_sb_definition.VALID_LOW_SBDEFINITION_JSON
    obj = test_sb_definition.create_test_low_sbdefinition()
    marshalled = CODEC.dumps(obj)

    assert_json_is_equal(marshalled, expected)


def test_read_a_low_sb_from_disk():
    """
    Test for loading an SBDefinition from a JSON file
    """
    cwd, _ = os.path.split(__file__)
    test_data = os.path.join(cwd, "common/testfile_sample_low_sb.json")
    result = CODEC.load_from_file(SBDefinition, test_data)
    expected = test_sb_definition.create_test_low_sbdefinition()
    assert result == expected


@pytest.mark.parametrize(
    "message_cls",
    [
        SBDefinition,
        SBDefinition,
    ],
)
def test_schema_registration(message_cls):
    """
    Verify that a schema is registered with the MarshmallowCodec.
    """
    assert message_cls in CODEC._schema  # pylint: disable=protected-access
