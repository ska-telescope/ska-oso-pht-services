"""
tests for the sdp_configuration schema to validate the
conversion between the JSON and Python representations
of the SDP configuration for an SKA Scheduling Block
"""

from ska_oso_pdm.entities.sdp import SDPConfiguration
from ska_oso_pdm.entities.sdp.processing_block import (
    PbDependency,
    ProcessingBlock,
    Workflow,
)
from ska_oso_pdm.entities.sdp.scan_type import Channel, ScanType
from ska_oso_pdm.schemas.sdp.sdp_configuration import SDPConfigurationSchema
from tests.unit.ska_oso_pdm.utils import assert_json_is_equal

VALID_SDP_CONFIG = """
{
  "eb_id": "eb-mvp01-20200325-00001",
  "max_length": 100.0,
  "scan_types": [
    {
      "scan_type_id": "science_A",
      "target": "sf1",
      "channels": [{
         "count": 744,
         "start": 0,
         "stride": 2,
         "freq_min": 0.35e9,
         "freq_max": 0.368e9,
         "link_map": [[0, 0], [200, 1], [744, 2], [944, 3]]
       },
       {
         "count": 744,
         "start": 2000,
         "stride": 1,
         "freq_min": 0.36e9,
         "freq_max": 0.368e9,
         "link_map": [[2000, 4], [2200, 5]]
       }]
    },
    {
      "scan_type_id": "calibration_B",
      "target": "sf2",
      "channels": [{
        "count": 744,
        "start": 0,
        "stride": 2,
        "freq_min": 0.35e9,
        "freq_max": 0.368e9,
        "link_map": [[0, 0], [200, 1], [744, 2], [944, 3]]
      },
      {
        "count": 744,
        "start": 2000,
        "stride": 1,
        "freq_min": 0.36e9,
        "freq_max": 0.368e9,
        "link_map": [[2000, 4], [2200, 5]]
      }]
    }
  ],
  "processing_blocks": [
    {
      "pb_id": "pb-mvp01-20200325-00001",
      "workflow": {"kind": "realtime", "name": "vis_receive", "version": "0.1.0"},
      "parameters": {}
    },
    {
      "pb_id": "pb-mvp01-20200325-00002",
      "workflow": {"kind": "realtime", "name": "test_realtime", "version": "0.1.0"},
      "parameters": {}
    },
    {
      "pb_id": "pb-mvp01-20200325-00003",
      "workflow": {"kind": "batch", "name": "ical", "version": "0.1.0"},
      "parameters": {},
      "dependencies": [
        {"pb_id": "pb-mvp01-20200325-00001", "kind": ["visibilities"]}
      ]
    },
    {
      "pb_id": "pb-mvp01-20200325-00004",
      "workflow": {"kind": "batch", "name": "dpreb", "version": "0.1.0"},
      "parameters": {},
      "dependencies": [
        {"pb_id": "pb-mvp01-20200325-00003", "kind": ["calibration"]}
      ]
    }
  ]
}"""


def sdp_config_for_test():  # pylint: disable=too-many-locals
    """
    Fixture which returns an SDPConfiguration object
    """
    # scan_type
    channel_1 = Channel(
        744, 0, 2, 0.35e9, 0.368e9, [(0, 0), (200, 1), (744, 2), (944, 3)]
    )
    channel_2 = Channel(744, 2000, 1, 0.36e9, 0.368e9, [(2000, 4), (2200, 5)])
    scan_type_a = ScanType("science_A", "sf1", [channel_1, channel_2])
    scan_type_b = ScanType("calibration_B", "sf2", [channel_1, channel_2])

    scan_types = [scan_type_a, scan_type_b]

    # PB workflow
    wf_a = Workflow("vis_receive", "realtime", "0.1.0")
    wf_b = Workflow("test_realtime", "realtime", "0.1.0")
    wf_c = Workflow("ical", "batch", "0.1.0")
    wf_d = Workflow("dpreb", "batch", "0.1.0")

    # PB Dependencies
    dep_a = PbDependency("pb-mvp01-20200325-00001", ["visibilities"])
    dep_b = PbDependency("pb-mvp01-20200325-00003", ["calibration"])

    # SDP Processing blocks
    pb_a = ProcessingBlock("pb-mvp01-20200325-00001", wf_a, {})
    pb_b = ProcessingBlock("pb-mvp01-20200325-00002", wf_b, {})
    pb_c = ProcessingBlock("pb-mvp01-20200325-00003", wf_c, {}, [dep_a])
    pb_d = ProcessingBlock("pb-mvp01-20200325-00004", wf_d, {}, [dep_b])

    processing_blocks = [pb_a, pb_b, pb_c, pb_d]

    return SDPConfiguration(
        "eb-mvp01-20200325-00001", 100.0, scan_types, processing_blocks
    )


def test_marshall_sdp_configuration():

    """
    Verify that SDPConfigurationSchema is marshalled to JSON correctly.
    """
    request = sdp_config_for_test()
    json_str = SDPConfigurationSchema().dumps(request)
    assert_json_is_equal(json_str, VALID_SDP_CONFIG)


def test_unmarshall_sdp_configuration():
    """
    Verify that JSON can be unmarshalled back to an SDPConfiguration
    object.
    """
    expected = sdp_config_for_test()
    request = SDPConfigurationSchema().loads(VALID_SDP_CONFIG)
    assert request == expected
