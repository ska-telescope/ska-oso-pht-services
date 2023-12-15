"""
Unit tests for the ska_oso_pdm.entities.sdp.scan_type module.
"""

from ska_oso_pdm.entities.sdp.scan_type import Channel, ScanType


def test_channel_equals():
    """
    Verify that Channel objects are considered equal when they have the same:
     - count
     - start
     - stride
     - freq_min
     - freq_max
     - link_map
    """
    channel1 = Channel(
        744, 0, 2, 0.35e9, 1.05e9, [(0, 0), (200, 1), (744, 2), (944, 3)]
    )
    channel2 = Channel(
        744, 0, 2, 0.35e9, 1.05e9, [(0, 0), (200, 1), (744, 2), (944, 3)]
    )
    assert channel1 == channel2

    assert channel1 != Channel(
        744, 2000, 2, 0.35e9, 1.05e9, [(0, 0), (200, 1), (744, 2), (944, 3)]
    )
    assert channel1 != Channel(
        744, 0, 1, 0.35e9, 1.05e9, [(0, 0), (200, 1), (744, 2), (944, 3)]
    )
    assert channel1 != Channel(
        744, 0, 2, 0.36e9, 1.04e9, [(0, 0), (200, 1), (744, 2), (944, 3)]
    )
    assert channel1 != Channel(744, 0, 2, 0.35e9, 1.05e9, [(2000, 4), (2200, 5)])


def test_channel_not_equal_to_other_objects():
    """
    Verify that Channel objects are not considered equal to objects of
    other types.
    """
    channel = Channel(744, 0, 2, 0.35e9, 1.05e9, [(0, 0), (200, 1), (744, 2), (944, 3)])
    assert channel != 1


def test_scan_type_equals():
    """
    Verify that ScanType objects are considered equal for the same passed parameter list
    """
    channel_1 = Channel(
        744, 0, 2, 0.35e9, 0.368e9, [(0, 0), (200, 1), (744, 2), (944, 3)]
    )
    channel_2 = Channel(744, 2000, 1, 0.36e9, 0.368e9, [(2000, 4), (2200, 5)])
    scan_type1 = ScanType("science_A", "123", [channel_1, channel_2])
    scan_type2 = ScanType("science_A", "123", [channel_1, channel_2])

    assert scan_type1 == scan_type2

    assert scan_type1 != ScanType("calibration_B", "123", [channel_1, channel_2])
    assert scan_type1 != ScanType("science_A", "1234", [channel_1, channel_2])
    assert scan_type1 != ScanType("science_A", "123", [channel_1])


def test_scan_type_not_equal_to_other_objects():
    """
    Verify that ScanType objects are not considered equal to objects of
    other types.
    """
    channel = Channel(
        744, 0, 2, 0.35e9, 0.368e9, [(0, 0), (200, 1), (744, 2), (944, 3)]
    )
    scan_type = ScanType("science_A", "123", [channel])
    assert scan_type != 1
