"""
tests for the scan_type schema to validate the
conversion between the JSON and Python representations
of the scan type section of an SDP configuration
"""
from ska_oso_pdm.entities.sdp.scan_type import Channel, ScanType
from ska_oso_pdm.schemas.sdp.scan_type import ChannelSchema, ScanTypeSchema
from tests.unit.ska_oso_pdm.utils import assert_json_is_equal

VALID_SCAN_TYPE_JSON = """
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
}
"""

VALID_CHANNEL_JSON = """
{
  "count": 744,
  "start": 0,
  "stride": 2,
  "freq_min": 0.35e9,
  "freq_max": 0.368e9,
  "link_map": [[0, 0], [200, 1], [744, 2], [944, 3]]
}
"""


def test_marshall_scan_type():
    """
    Verify that ScanTypeSchema is marshalled to JSON correctly.
    """
    channel_1 = Channel(
        744, 0, 2, 0.35e9, 0.368e9, [(0, 0), (200, 1), (744, 2), (944, 3)]
    )
    channel_2 = Channel(744, 2000, 1, 0.36e9, 0.368e9, [(2000, 4), (2200, 5)])
    request = ScanType("science_A", "sf1", [channel_1, channel_2])
    json_str = ScanTypeSchema().dumps(request)
    assert_json_is_equal(json_str, VALID_SCAN_TYPE_JSON)


def test_unmarshall_scan_type():
    """
    Verify that JSON can be unmarshalled back to an ScanType
    object.
    """
    channel_1 = Channel(
        744, 0, 2, 0.35e9, 0.368e9, [(0, 0), (200, 1), (744, 2), (944, 3)]
    )
    channel_2 = Channel(744, 2000, 1, 0.36e9, 0.368e9, [(2000, 4), (2200, 5)])
    expected = ScanType("science_A", "sf1", [channel_1, channel_2])
    request = ScanTypeSchema().loads(VALID_SCAN_TYPE_JSON)
    assert request == expected


def test_marshall_channel():

    """
    Verify that ChannelSchema is marshalled to JSON correctly.
    """
    request = Channel(
        744, 0, 2, 0.35e9, 0.368e9, [(0, 0), (200, 1), (744, 2), (944, 3)]
    )
    json_str = ChannelSchema().dumps(request)
    assert_json_is_equal(json_str, VALID_CHANNEL_JSON)


def test_unmarshall_channel():
    """
    Verify that JSON can be unmarshalled back to an Channel object.
    """
    expected = Channel(
        744, 0, 2, 0.35e9, 0.368e9, [(0, 0), (200, 1), (744, 2), (944, 3)]
    )
    request = ChannelSchema().loads(VALID_CHANNEL_JSON)
    assert request == expected
