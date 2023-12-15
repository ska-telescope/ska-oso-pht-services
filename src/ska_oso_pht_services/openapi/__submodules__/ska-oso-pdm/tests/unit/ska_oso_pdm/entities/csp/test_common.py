"""
Unit tests for the ska_oso_pdm.entities.csp_configuration module.
"""
import functools
import itertools

import pytest

from ska_oso_pdm.entities.csp.common import (
    CBFConfiguration,
    CommonConfiguration,
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    SubarrayConfiguration,
)


def test_common_configuration_equals():
    """
    Verify that CommonConfiguration objects are considered equal when all
    attributes are equal.
    """
    subarray_id = 1
    band_5_tuning = [5.85, 7.25]

    config1 = CommonConfiguration(subarray_id, band_5_tuning)
    config2 = CommonConfiguration(subarray_id, band_5_tuning)
    assert config1 == config2

    assert config1 != CommonConfiguration(2)
    assert config1 != CommonConfiguration(1, [5.0, 7.0])


def test_common_configuration_not_equal_to_other_objects():
    """
    Verify that CommonConfiguration objects are not considered equal to objects
    of other types.
    """
    subarray_id = 1
    band_5_tuning = [5.85, 7.25]
    config = CommonConfiguration(subarray_id, band_5_tuning)
    assert config != 1


def test_subarray_configuration_equals():
    """
    Verify that SubarrayConfiguration objects are considered equal when all
    attributes are equal.
    """
    subarray_name = "Test Subarray"

    config1 = SubarrayConfiguration(subarray_name)
    config2 = SubarrayConfiguration(subarray_name)
    assert config1 == config2

    assert config1 != SubarrayConfiguration("Test Subarray2")


def test_subarray_configuration_not_equal_to_other_objects():
    """
    Verify that SubarrayConfiguration objects are not considered equal to objects
    of other types.
    """
    subarray_name = "Test Subarray"
    config = SubarrayConfiguration(subarray_name)
    assert config != 1


def test_cbf_configuration_equals():
    """
    Verify that CBFConfiguration objects are considered equal when all
    attributes are equal.
    """
    fsp = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1, 0)

    config1 = CBFConfiguration([fsp])
    config2 = CBFConfiguration([fsp])
    assert config1 == config2

    assert config1 != CBFConfiguration([fsp, fsp])


def test_cbf_configuration_not_equal_to_other_objects():
    """
    Verify that CBFConfiguration objects are not considered equal to objects
    of other types.
    """
    fsp = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1, 0)
    config = CBFConfiguration([fsp])
    assert config != 1


def test_fsp_configuration_equals():
    """
    Verify that FSPConfigurations are considered equal when all attributes are
    equal.
    """
    fsp_id = 1
    mode = FSPFunctionMode.CORR
    slice_id = 1
    bandwidth = 0
    channel_avg_map = list(zip(itertools.count(1, 744), 20 * [0]))
    integration_factor = 1
    output_link_map = list(zip(itertools.count(1, 200), 2 * [0]))
    channel_offset = 744

    config1 = FSPConfiguration(
        fsp_id, mode, slice_id, integration_factor, bandwidth, channel_avg_map
    )
    config2 = FSPConfiguration(
        fsp_id, mode, slice_id, integration_factor, bandwidth, channel_avg_map
    )
    config3 = FSPConfiguration(
        fsp_id,
        mode,
        slice_id,
        integration_factor,
        bandwidth,
        channel_avg_map,
        output_link_map,
        channel_offset,
    )
    assert config1 != config3

    assert config1 == config2

    assert config1 != FSPConfiguration(
        2, mode, slice_id, integration_factor, bandwidth, channel_avg_map
    )
    assert config1 != FSPConfiguration(
        fsp_id,
        FSPFunctionMode.PSS_BF,
        slice_id,
        integration_factor,
        bandwidth,
        channel_avg_map,
    )
    assert config1 != FSPConfiguration(
        fsp_id, mode, 2, integration_factor, bandwidth, channel_avg_map
    )
    assert config1 != FSPConfiguration(
        fsp_id, mode, slice_id, 10, bandwidth, channel_avg_map
    )
    assert config1 != FSPConfiguration(
        fsp_id,
        mode,
        slice_id,
        integration_factor,
        1,
        channel_avg_map,
        zoom_window_tuning=470000,
    )
    assert config1 != FSPConfiguration(
        fsp_id,
        mode,
        slice_id,
        integration_factor,
        bandwidth,
        list(zip(itertools.count(1, 744), 20 * [1])),
    )


def test_fsp_configuration_not_equal_to_other_objects():
    """
    Verify that FSPConfiguration objects are not considered equal to objects
    of other types.
    """
    config = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1, 0)
    assert config != 1


def test_csp_configuration_equals():
    """
    Verify that CSPConfiguration objects are considered equal when all
    attributes are equal.
    """
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    fsp = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1, 0)
    fsp2 = FSPConfiguration(1, FSPFunctionMode.CORR, 2, 1, 0)

    config1 = CSPConfiguration(csp_id, [fsp])
    config2 = CSPConfiguration(csp_id, [fsp])
    assert config1 == config2

    assert config1 != CSPConfiguration(csp_id, [fsp2])
    assert config1 != CSPConfiguration(csp_id, [fsp, fsp])


def test_csp_configuration_equals_with_all_parameters():
    """
    Verify that CSPConfiguration objects are considered equal when all
    attributes are equal.
    """
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    fsp = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1, 0)
    subarray_id = 1
    band_5_tuning = [5.85, 7.25]
    subarray_name = "Test Subarray"
    subarray_config = SubarrayConfiguration(subarray_name)
    common_config = CommonConfiguration(subarray_id, band_5_tuning)
    cbf_config = CBFConfiguration([fsp])
    pst_config = None
    pss_config = None

    config1 = CSPConfiguration(csp_id, [fsp])
    config2 = CSPConfiguration(csp_id, [fsp])

    config3 = CSPConfiguration(
        config_id="foo",
        subarray_config=subarray_config,
        common_config=common_config,
        cbf_config=cbf_config,
        pst_config=pst_config,
        pss_config=pss_config,
    )
    config4 = CSPConfiguration(
        config_id="foo",
        subarray_config=subarray_config,
        common_config=common_config,
        cbf_config=cbf_config,
        pst_config=pst_config,
        pss_config=pss_config,
    )

    assert config1 == config2
    assert config3 == config4

    assert config1 != CSPConfiguration("jeff", [fsp])
    assert config3 != CSPConfiguration(
        subarray_config=subarray_config,
        common_config=common_config,
        cbf_config=cbf_config,
    )


def test_csp_configuration_not_equal_to_other_objects():
    """
    Verify that CSPConfiguration objects are not considered equal to objects
    of other types.
    """
    csp_id = "sbi-mvp01-20200325-00001-science_A"
    fsp = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1, 0)
    config = CSPConfiguration(csp_id, [fsp])
    assert config != 1


def test_fsp_id_range():
    """
    Verify that fsp id is in the range of 1 to 27
    """
    fsp_id = 0
    with pytest.raises(ValueError):
        _ = FSPConfiguration(fsp_id, FSPFunctionMode.CORR, 1, 1, 0)
    fsp_id = 28
    with pytest.raises(ValueError):
        _ = FSPConfiguration(fsp_id, FSPFunctionMode.CORR, 1, 1, 0)


def test_fsp_slice_id_range():
    """
    Verify that fsp slice id is in the range of 1 to 26
    """
    fsp_slice_id = 0
    with pytest.raises(ValueError):
        _ = FSPConfiguration(1, FSPFunctionMode.CORR, fsp_slice_id, 1, 0)
    fsp_slice_id = 27
    with pytest.raises(ValueError):
        _ = FSPConfiguration(1, FSPFunctionMode.CORR, fsp_slice_id, 1, 0)


def test_corr_bandwidth_range():
    """
    Verify that zoom_factor is in the range of 0 to 6
    """
    zoom_factor = -1
    with pytest.raises(ValueError):
        _ = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1, zoom_factor)
    zoom_factor = 7
    with pytest.raises(ValueError):
        _ = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1, zoom_factor)


def test_integration_time_is_within_limits():
    """
    Verify that integration time is no greater than 1
    """
    _ = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1, 0)
    with pytest.raises(ValueError):
        _ = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 0, 0)
    with pytest.raises(ValueError):
        _ = FSPConfiguration(1, FSPFunctionMode.CORR, 1, 1540, 0)


def test_number_of_channel_avg_mapping_tuples():
    """
    Verify that FSPConfiguration fails if there are an invalid number of
    entries in the channel average mapping argument.
    """
    fsp_constructor = functools.partial(
        FSPConfiguration, 1, FSPFunctionMode.CORR, 1, 140, 0
    )
    # test for 21 tuples
    channel_avg_map = list(zip(itertools.count(1, 744), 21 * [0]))
    with pytest.raises(ValueError):
        _ = fsp_constructor(channel_avg_map)


def test_zoom_window_tuning_is_none():
    """
    Verify that zoom window tuning is none when Correlator bandwidth is greather than 0
    """
    zoom_window_tuning = None
    with pytest.raises(ValueError):
        _ = FSPConfiguration(
            1, FSPFunctionMode.CORR, 1, 1, 1, zoom_window_tuning=zoom_window_tuning
        )
