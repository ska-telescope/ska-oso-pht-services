"""
The entities.csp_configuration module defines
a simple Python representation of CSP and FSP
configurations.
"""
import enum
from typing import List, Optional, Tuple

__all__ = [
    "CSPConfiguration",
    "CSPConfigurationID",
    "FSPConfiguration",
    "FSPFunctionMode",
    "CBFConfiguration",
    "SubarrayConfiguration",
    "CommonConfiguration",
]

# aliases to str for entity IDs
CSPConfigurationID = str

# Global constants for FSP configurations
MAX_FSP_ID = 27
MAX_FREQUENCY_SLICE_ID = 26
MIN_CORR_BANDWIDTH = 0
MAX_CORR_BANDWIDTH = 6
MAX_TUPLE_COUNT_IN_CHANNEL_MAP = 20


class FSPFunctionMode(enum.Enum):
    """
    FSPFunctionMode is an enumeration of the available FSP modes.
    """

    CORR = "CORR"
    PSS_BF = "PSS-BF"
    PST_BF = "PST-BF"
    VLBI = "VLBI"


class FSPConfiguration:  # pylint: disable=too-many-instance-attributes
    """
    FSPConfiguration defines the configuration for a CSP Frequency Slice
    Processor.
    """

    # pylint: disable=too-many-arguments
    def __init__(
        self,
        fsp_id: int,
        function_mode: FSPFunctionMode,
        frequency_slice_id: int,
        integration_factor: int,
        zoom_factor: int,
        channel_averaging_map: List[Tuple] = None,
        output_link_map: List[Tuple] = None,
        channel_offset: int = None,
        zoom_window_tuning: int = None,
    ):

        """
        Create a new FSPConfiguration.

        Channel averaging map is an optional list of 20 x (int,int) tuples.


        :param fsp_id: FSP configuration ID [1..27]
        :param function_mode: FSP function mode
        :param frequency_slice_id: frequency slicer ID [1..26]
        :param zoom_factor: zoom factor [0..6]
        :param integration_factor: integer multiple of correlation integration time (140ms) [1..10]
        :param channel_averaging_map: Optional channel averaging map
        :param output_link_map: Optional output_link_map
        :param channel_offset: Optional channel offset value in integer
        :param zoom_window_tuning: Optional zoom window tuning value in integer
        """

        if not 1 <= fsp_id <= MAX_FSP_ID:
            raise ValueError(f"FSP ID must be in range 1..{MAX_FSP_ID}. Got {fsp_id}")
        self.fsp_id = fsp_id

        self.function_mode = function_mode

        if not 1 <= frequency_slice_id <= MAX_FREQUENCY_SLICE_ID:
            raise ValueError(
                f"Frequency slice ID must be in range 1..{MAX_FREQUENCY_SLICE_ID}. "
                f"Got {frequency_slice_id}"
            )
        self.frequency_slice_id = frequency_slice_id

        if not MIN_CORR_BANDWIDTH <= zoom_factor <= MAX_CORR_BANDWIDTH:
            raise ValueError(
                f"Correlator bandwidth must be in range "
                f"{MIN_CORR_BANDWIDTH}..{MAX_CORR_BANDWIDTH}. "
                f"Got {zoom_factor}"
            )
        self.zoom_factor = zoom_factor

        if not 1 <= integration_factor <= 10:
            msg = f"Integration factor must in range 1..10. Got {integration_factor}"
            raise ValueError(msg)
        self.integration_factor = integration_factor

        if (
            channel_averaging_map
            and len(channel_averaging_map) > MAX_TUPLE_COUNT_IN_CHANNEL_MAP
        ):
            raise ValueError(
                f"Number of tuples in channel averaging map must be "
                f"{MAX_TUPLE_COUNT_IN_CHANNEL_MAP}. "
                f"Got {len(channel_averaging_map)}"
            )

        self.channel_averaging_map = channel_averaging_map
        self.output_link_map = output_link_map
        self.channel_offset = channel_offset

        if zoom_window_tuning is None and zoom_factor > 0:
            raise ValueError(
                "Zoom window tuning can not be None when Correlator bandwidth"
                " is greater than 0"
            )

        self.zoom_window_tuning = zoom_window_tuning

    def __eq__(self, other):
        if not isinstance(other, FSPConfiguration):
            return False
        return (
            self.fsp_id == other.fsp_id
            and self.function_mode == other.function_mode
            and self.frequency_slice_id == other.frequency_slice_id
            and self.zoom_factor == other.zoom_factor
            and self.integration_factor == other.integration_factor
            and self.channel_averaging_map == other.channel_averaging_map
            and self.output_link_map == other.output_link_map
            and self.channel_offset == other.channel_offset
            and self.zoom_window_tuning == other.zoom_window_tuning
        )

    def __repr__(self):
        return (
            f"<FSPConfiguration("
            f"fsp_id={self.fsp_id}, "
            f"function_mode={self.function_mode}, "
            f"frequency_slice_id={self.frequency_slice_id}, "
            f"zoom_factor={self.zoom_factor}, "
            f"integration_factor={self.integration_factor}, "
            f"channel_averaging_map={self.channel_averaging_map}, "
            f"output_link_map={self.output_link_map}, "
            f"channel_offset={self.channel_offset}, "
            f"zoom_window_tuning={self.zoom_window_tuning})>"
        )


class SubarrayConfiguration:
    """
    Class to hold the parameters relevant only for the current sub-array device.
    """

    def __init__(self, subarray_name: str):
        """
        Create sub-array device configuration.
        :param sub-array_name: Name of the sub-array
        """
        self.subarray_name = subarray_name

    def __eq__(self, other):
        if not isinstance(other, SubarrayConfiguration):
            return False
        return self.subarray_name == other.subarray_name

    def __repr__(self):
        return f"<SubarrayConfiguration(" f"subarray_name={self.subarray_name})>"


class CommonConfiguration:
    """
    Class to hold the CSP sub-elements.
    """

    def __init__(
        self,
        subarray_id: Optional[int] = None,
        band_5_tuning: Optional[List[float]] = None,
    ):
        """
        Create a new CSPConfiguration.

        :param subarray_id: an ID of sub-array device (optional)
        :param band_5_tuning: List of integer (optional)
        """
        self.subarray_id = subarray_id
        self.band_5_tuning = band_5_tuning

    def __eq__(self, other):
        if not isinstance(other, CommonConfiguration):
            return False
        return (
            self.subarray_id == other.subarray_id
            and self.band_5_tuning == other.band_5_tuning
        )

    def __repr__(self):
        return (
            f"<CommonConfiguration("
            f"subarray_id={self.subarray_id}, "
            f"band_5_tuning={self.band_5_tuning})>"
        )


class VLBIConfiguration:
    """
    Class to hold VLBI configurations.
    """


class CBFConfiguration:
    """
    Class to hold all FSP and VLBI configurations.
    """

    def __init__(
        self,
        fsp_configs: List[FSPConfiguration],
        vlbi_config: Optional[VLBIConfiguration] = None,
    ):
        """
        Create a new CBFConfiguration.
        :param fsp_configs: the FSP configurations to set
        :param vlbi_config: the VLBI configurations to set (optional)
        """
        self.fsp_configs = fsp_configs
        self.vlbi_config = vlbi_config

    def __eq__(self, other):
        if not isinstance(other, CBFConfiguration):
            return False
        return (
            self.fsp_configs == other.fsp_configs
            and self.vlbi_config == other.vlbi_config
        )

    def __repr__(self):
        return (
            f"<CommonConfiguration("
            f"fsp_configs={self.fsp_configs}, "
            f"vlbi_config={self.vlbi_config})>"
        )


class PSTConfiguration:
    """
    Class to hold PST configurations.
    """


class PSSConfiguration:
    """
    Class to hold PSS configurations.
    """


class CSPConfiguration:
    """
    Class to hold all CSP configuration.
    """

    def __init__(
        self,
        config_id: CSPConfigurationID = None,
        subarray_config: SubarrayConfiguration = None,
        common_config: CommonConfiguration = None,
        cbf_config: CBFConfiguration = None,
        pst_config: PSTConfiguration = None,
        pss_config: PSSConfiguration = None,
    ):  # pylint: disable=too-many-arguments
        """
        Create a new CSPConfiguration.

        :param config_id: an ID for CSP configuration
        :param subarray_config: Sub-array configuration to set
        :param common_config: the common CSP elemenets to set
        :param cbf_config: the CBF configurations to set
        :param pst_config: the PST configurations to set
        :param pss_config: the PSS configurations to set
        """
        self.config_id = config_id
        self.subarray_config = subarray_config
        self.common_config = common_config
        self.cbf_config = cbf_config
        self.pst_config = pst_config
        self.pss_config = pss_config

    def __eq__(self, other):
        if not isinstance(other, CSPConfiguration):
            return False
        return (
            self.config_id == other.config_id
            and self.subarray_config == other.subarray_config
            and self.common_config == other.common_config
            and self.cbf_config == other.cbf_config
            and self.pst_config == other.pst_config
            and self.pss_config == other.pss_config
        )

    def __repr__(self):
        return (
            f"<CSPConfiguration(config_id={self.config_id}, subarray_config"
            f"={self.subarray_config}, "
            f"common_config={self.common_config}, "
            f"cbf_config={self.cbf_config}, "
            f"pst_config={self.pst_config}, "
            f"pss_config={self.pss_config})>"
        )
