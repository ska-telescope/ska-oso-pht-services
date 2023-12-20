"""
tests for the csp configuration schema to validate the
conversion between the JSON and Python representations
of the csp configuration section of an SKA Scheduling Block
"""
from ska_oso_pdm.entities.csp.common import (
    CBFConfiguration,
    CommonConfiguration,
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    SubarrayConfiguration,
)
from ska_oso_pdm.schemas.csp.common import (
    CBFConfigurationSchema,
    CommonConfigurationSchema,
    CSPConfigurationSchema,
    FSPConfigurationSchema,
    SubarrayConfigurationSchema,
)
from tests.unit.ska_oso_pdm.utils import assert_json_is_equal

VALID_CSPCONFIGURATION_JSON = """
{
  "config_id": "jeff",
  "subarray": {
    "subarray_name": "science period 23"
  },
  "common": {
    "subarray_id": 1,
    "band_5_tuning": [5.85, 7.25]
  },
  "cbf": {
    "fsp": [
      {
        "fsp_id": 1,
        "function_mode": "CORR",
        "frequency_slice_id": 1,
        "integration_factor" : 1,
        "zoom_factor": 0
      },
      {
        "fsp_id": 2,
        "function_mode": "CORR",
        "frequency_slice_id": 2,
        "integration_factor" : 1,
        "zoom_factor": 1,
        "zoom_window_tuning":4700000
      }
    ]
  }
}
"""


def test_marshall_cspconfiguration():
    """
    Verify that CSPConfiguration is marshalled to JSON correctly.
    """
    fsp_1 = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1, 0)
    fsp_2 = FSPConfiguration(
        2, FSPFunctionMode.CORR, 2, 1, 1, zoom_window_tuning=4700000
    )
    cbf_config = CBFConfiguration([fsp_1, fsp_2])
    csp_subarray_config = SubarrayConfiguration("science period 23")
    csp_common_config = CommonConfiguration(1, [5.85, 7.25])
    csp_config = CSPConfiguration(
        config_id="jeff",
        subarray_config=csp_subarray_config,
        common_config=csp_common_config,
        cbf_config=cbf_config,
    )
    schema = CSPConfigurationSchema()
    marshalled = schema.dumps(csp_config)
    assert_json_is_equal(marshalled, VALID_CSPCONFIGURATION_JSON)


def test_unmarshall_cspconfiguration():
    """
    Verify that CSPConfiguration is unmarshalled from JSON correctly.
    """
    fsp_1 = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1, 0)
    fsp_2 = FSPConfiguration(
        2, FSPFunctionMode.CORR, 2, 1, 1, zoom_window_tuning=4700000
    )
    cbf_config = CBFConfiguration([fsp_1, fsp_2])
    csp_subarray_config = SubarrayConfiguration("science period 23")
    csp_common_config = CommonConfiguration(1, [5.85, 7.25])
    csp_config = CSPConfiguration(
        config_id="jeff",
        subarray_config=csp_subarray_config,
        common_config=csp_common_config,
        cbf_config=cbf_config,
    )
    schema = CSPConfigurationSchema()
    unmarshalled = schema.loads(VALID_CSPCONFIGURATION_JSON)

    assert csp_config == unmarshalled


VALID_FSPCONFIGURATION_JSON = """
{
  "fsp_id": 2,
  "function_mode": "CORR",
  "frequency_slice_id": 2,
  "integration_factor": 1,
  "zoom_factor": 1,
  "output_link_map": [[0,4], [200,5]],
  "channel_averaging_map": [[0, 2], [744, 0]],
  "channel_offset": 744,
  "zoom_window_tuning": 4700000
}"""


def test_marshall_fsp_configuration():
    """
    Verify that FSPConfiguration is marshalled to JSON correctly.
    """
    fsp_config = FSPConfiguration(
        2,
        FSPFunctionMode.CORR,
        2,
        1,
        1,
        channel_averaging_map=[(0, 2), (744, 0)],
        channel_offset=744,
        output_link_map=[(0, 4), (200, 5)],
        zoom_window_tuning=4700000,
    )
    schema = FSPConfigurationSchema()
    marshalled = schema.dumps(fsp_config)

    assert_json_is_equal(marshalled, VALID_FSPCONFIGURATION_JSON)


def test_unmarshall_fsp_configuration():
    """
    Verify that FSPConfiguration is marshalled to JSON correctly.
    """
    fsp_config = FSPConfiguration(
        2,
        FSPFunctionMode.CORR,
        2,
        1,
        1,
        channel_averaging_map=[(0, 2), (744, 0)],
        channel_offset=744,
        output_link_map=[(0, 4), (200, 5)],
        zoom_window_tuning=4700000,
    )
    unmarshalled = FSPConfigurationSchema().loads(VALID_FSPCONFIGURATION_JSON)

    assert fsp_config == unmarshalled


def test_marshall_fsp_configuration_with_null_channel_averaging_map():
    """
    Verify that the channel_averaging_map FSPConfiguration directive is
    removed when not set.
    """
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1, 0)
    schema = FSPConfigurationSchema()
    marshalled = schema.dumps(fsp_config)
    assert "channel_averaging_map" not in marshalled


def test_marshall_fsp_configuration_with_null_output_link_map():
    """
    Verify that the output_link_map FSPConfiguration directive is
    removed when not set.
    """
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1, 0)
    schema = FSPConfigurationSchema()
    marshalled = schema.dumps(fsp_config)
    assert "output_link_map" not in marshalled


def test_marshall_fsp_configuration_with_null_fsp_channel_offset():
    """
    Verify that the channel_offset FSPConfiguration directive is
    removed when not set.
    """
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1, 0)
    schema = FSPConfigurationSchema()
    marshalled = schema.dumps(fsp_config)
    assert "channel_offset" not in marshalled


def test_marshall_fsp_configuration_with_null_zoom_window_tuning():
    """
    Verify that the zoom_window_tuning FSPConfiguration directive is
    removed when not set.
    """
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1, 0)
    schema = FSPConfigurationSchema()
    marshalled = schema.dumps(fsp_config)
    assert "zoom_window_tuning" not in marshalled


# def test_marshall_cspconfiguration_does_not_modify_original():
#     """
#     Verify that serialising a CspConfiguration does not change the object.
#     """
#     config = CSPConfiguration(
#         'csp ID goes here',
#         [FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1, 0)]
#     )
#     original_config = copy.deepcopy(config)
#     CSPConfigurationSchema().dumps(config)
#     assert config == original_config

VALID_SUBARRAYCONFIGURATION_JSON = """
{
  "subarray_name": "Test Subarray"
}
"""


def test_marshall_subarray_configuration():
    """
    Verify that SubarrayConfiguration is marshalled to JSON correctly.
    """
    subarray_config = SubarrayConfiguration("Test Subarray")
    schema = SubarrayConfigurationSchema()
    marshalled = schema.dumps(subarray_config)
    assert_json_is_equal(marshalled, VALID_SUBARRAYCONFIGURATION_JSON)


def test_unmarshall_subarray_configuration():
    """
    Verify that SubarrayConfiguration is unmarshalled from JSON correctly.
    """
    subarray_config = SubarrayConfiguration("Test Subarray")
    schema = SubarrayConfigurationSchema()
    unmarshalled = schema.loads(VALID_SUBARRAYCONFIGURATION_JSON)

    assert subarray_config == unmarshalled


########################
# CommonConfiguration tests
########################

VALID_COMMONCONFIGURATION_JSON = """
{
  "subarray_id": 1,
  "band_5_tuning": [5.85, 7.25]
}
"""


def test_marshall_common_configuration():
    """
    Verify that CommonConfiguration is marshalled to JSON correctly.
    """
    common_config = CommonConfiguration(1, [5.85, 7.25])
    schema = CommonConfigurationSchema()
    marshalled = schema.dumps(common_config)
    assert_json_is_equal(marshalled, VALID_COMMONCONFIGURATION_JSON)


def test_unmarshall_common_configuration():
    """
    Verify that CommonConfiguration is unmarshalled from JSON correctly.
    """
    common_config = CommonConfiguration(1, [5.85, 7.25])
    schema = CommonConfigurationSchema()
    unmarshalled = schema.loads(VALID_COMMONCONFIGURATION_JSON)

    assert common_config == unmarshalled


########################
# CBFConfiguration tests
########################

VALID_CBFCONFIGURATION_JSON = """
{
  "fsp": [
    {
      "fsp_id": 1,
      "function_mode": "CORR",
      "frequency_slice_id": 1,
      "integration_factor" : 1,
      "zoom_factor": 0
    }
  ]
}
"""


def test_marshall_cbf_configuration():
    """
    Verify that CBFConfiguration is marshalled to JSON correctly.
    """
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1, 0)
    cbf_config = CBFConfiguration([fsp_config])
    schema = CBFConfigurationSchema()
    marshalled = schema.dumps(cbf_config)
    assert_json_is_equal(marshalled, VALID_CBFCONFIGURATION_JSON)


def test_unmarshall_cbf_configuration():
    """
    Verify that CBFConfiguration is unmarshalled from JSON correctly.
    """
    fsp_config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1, 0)
    cbf_config = CBFConfiguration([fsp_config])
    schema = CBFConfigurationSchema()
    unmarshalled = schema.loads(VALID_CBFCONFIGURATION_JSON)

    assert cbf_config == unmarshalled
