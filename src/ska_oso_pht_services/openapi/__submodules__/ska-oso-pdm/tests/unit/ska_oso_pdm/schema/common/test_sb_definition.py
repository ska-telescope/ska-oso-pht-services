"""
tests for the scheduling_block_schema to validate the
conversion between the JSON and Python representations
of an SKA Scheduling Block
"""

import os
from copy import deepcopy
from datetime import datetime, timedelta, timezone

from ska_oso_pdm.entities.common.procedures import (
    FilesystemScript,
    GitScript,
    PythonArguments,
)
from ska_oso_pdm.entities.common.sb_definition import (
    MetaData,
    SBDefinition,
    TelescopeType,
)
from ska_oso_pdm.entities.common.scan_definition import ScanDefinition
from ska_oso_pdm.entities.common.target import (
    EquatorialCoordinates,
    FivePointParameters,
    HorizontalCoordinates,
    PointingPattern,
    RasterParameters,
    SinglePointParameters,
    StarRasterParameters,
    Target,
)
from ska_oso_pdm.entities.csp.common import (
    CBFConfiguration,
    CommonConfiguration,
    CSPConfiguration,
    FSPConfiguration,
    FSPFunctionMode,
    SubarrayConfiguration,
)
from ska_oso_pdm.entities.dish.dish_allocation import DishAllocation
from ska_oso_pdm.entities.dish.dish_configuration import DishConfiguration, ReceiverBand
from ska_oso_pdm.entities.mccs.mccs_allocation import MCCSAllocation
from ska_oso_pdm.entities.mccs.subarray_beam_configuration import (
    SubarrayBeamConfiguration,
)
from ska_oso_pdm.entities.mccs.target_beam_configuration import TargetBeamConfiguration
from ska_oso_pdm.entities.sdp import SDPConfiguration
from ska_oso_pdm.entities.sdp.processing_block import (
    PbDependency,
    ProcessingBlock,
    Workflow,
)
from ska_oso_pdm.entities.sdp.scan_type import Channel, ScanType
from ska_oso_pdm.schemas.common.sb_definition import MetaDataSchema, SBDefinitionSchema
from tests.unit.ska_oso_pdm.utils import assert_json_is_equal

METADATA_JSON = """
{
    "created_by": "Liz Bartlett",
    "created_on": "2022-04-27T23:20:47.922400",
    "version": 1
}
"""

metadata = MetaData(
    created_by="Liz Bartlett", created_on=datetime(2022, 4, 27, 23, 20, 47, 922400)
)


def test_marshall_metadata():
    """
    Verify that MetaData is marshalled to JSON correctly
    """
    assert_json_is_equal(METADATA_JSON, MetaDataSchema().dumps(metadata))


def test_unmarshall_metadata():
    """
    Verify that JSON can be unmarshalled to a MetaData object
    """
    expected = MetaDataSchema().loads(METADATA_JSON)
    assert expected == metadata


def create_test_mid_sbdefinition():  # pylint: disable=too-many-locals too-many-statements
    """
    Utility method to create a valid MID sb configuration for use in unit test
    """
    sbd = SBDefinition(
        sbd_id="sbi-mvp01-20200325-00001",
        telescope=TelescopeType.MID,
        activities={
            "allocate": FilesystemScript(
                path="/path/to/allocatescript.py",
                function_args={
                    "init": PythonArguments(
                        args=["posarg1", "posarg2"], kwargs={"argname": "argval"}
                    ),
                    "main": PythonArguments(
                        args=["posarg1", "posarg2"], kwargs={"argname": "argval"}
                    ),
                },
            ),
            "observe": GitScript(
                repo="https://gitlab.com/script_repo/operational_scripts",
                path="/relative/path/to/scriptinsiderepo.py",
                branch="main",
                function_args={
                    "init": PythonArguments(
                        args=["posarg1", "posarg2"], kwargs={"argname": "argval"}
                    ),
                    "main": PythonArguments(
                        args=["posarg1", "posarg2"], kwargs={"argname": "argval"}
                    ),
                },
            ),
        },
    )

    # Add metadata
    sbd.metadata.created_on = datetime(
        2022, 3, 28, 15, 43, 53, 971548, tzinfo=timezone.utc
    )
    sbd.metadata.created_by = "Liz Bartlett"
    sbd.metadata.last_modified_on = datetime(
        2022, 3, 28, 15, 43, 53, 971548, tzinfo=timezone.utc
    )
    sbd.metadata.last_modified_by = "Liz Bartlett"

    # Add csp_configuration
    fsp_1 = FSPConfiguration(
        fsp_id=1,
        function_mode=FSPFunctionMode.CORR,
        frequency_slice_id=1,
        integration_factor=1,
        zoom_factor=0,
        channel_averaging_map=[(0, 2), (744, 0)],
        output_link_map=[(0, 0), (200, 1)],
        channel_offset=0,
    )
    fsp_2 = FSPConfiguration(
        fsp_id=2,
        function_mode=FSPFunctionMode.CORR,
        frequency_slice_id=2,
        integration_factor=1,
        zoom_factor=1,
        zoom_window_tuning=650000,
    )

    csp_config = CSPConfiguration(
        config_id="csp-mvp01-20220329-00001",
        subarray_config=SubarrayConfiguration("science period 23"),
        common_config=CommonConfiguration(1, [5.85, 7.25]),
        cbf_config=CBFConfiguration([fsp_1, fsp_2]),
    )

    sbd.csp_configurations = [csp_config]

    calibrator_target = Target(
        target_id="Polaris Australis",
        reference_coordinate=EquatorialCoordinates(ra="21:08:47.92", dec="-88:57:22.9"),
        pointing_pattern=PointingPattern(
            active=FivePointParameters.kind,
            parameters=[
                FivePointParameters(offset_arcsec=5.0),
                RasterParameters(
                    row_length_arcsec=1.23,
                    row_offset_arcsec=4.56,
                    n_rows=2,
                    pa=7.89,
                    unidirectional=True,
                ),
                StarRasterParameters(
                    row_length_arcsec=1.23,
                    n_rows=2,
                    row_offset_angle=4.56,
                    unidirectional=True,
                ),
            ],
        ),
    )

    science_target = Target(
        target_id="M83",
        reference_coordinate=EquatorialCoordinates(
            ra="13:37:00.919", dec="-29:51:56.74"
        ),
        pointing_pattern=PointingPattern(
            active=SinglePointParameters.kind, parameters=[SinglePointParameters()]
        ),
    )

    sbd.targets = [calibrator_target, science_target]

    # Add scan_definitions
    calibrator_scan = ScanDefinition(
        scan_definition_id="calibrator scan",
        scan_duration=timedelta(seconds=60.0),
        csp_configuration_id=csp_config.config_id,
        target_id=calibrator_target.target_id,
        dish_configuration_id="dish config 123",
        scan_type_id="calibration_B",
    )
    science_scan = ScanDefinition(
        scan_definition_id="science scan",
        scan_duration=timedelta(seconds=60.0),
        target_id=science_target.target_id,
        dish_configuration_id="dish config 123",
        scan_type_id="science_A",
    )

    sbd.scan_definitions.append(calibrator_scan)
    sbd.scan_definitions.append(science_scan)

    sbd.scan_sequence = [
        calibrator_scan.scan_definition_id,
        science_scan.scan_definition_id,
        science_scan.scan_definition_id,
        calibrator_scan.scan_definition_id,
    ]

    # Add sdp_configuration
    channel_1 = Channel(
        744, 0, 2, 0.35e9, 0.368e9, [(0, 0), (200, 1), (744, 2), (944, 3)]
    )
    channel_2 = Channel(744, 2000, 1, 0.36e9, 0.368e9, [(2000, 4), (2200, 5)])
    scan_type_a = ScanType("science_A", "my science target", [channel_1, channel_2])
    scan_type_b = ScanType(
        "calibration_B", "my calibrator target", [channel_1, channel_2]
    )

    scan_types = [scan_type_a, scan_type_b]

    # PB workflow
    wf_a = Workflow("vis_receive", "realtime", "0.1.0")
    wf_b = Workflow("test_receive_addresses", "realtime", "0.3.2")
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

    sdp_configuration = SDPConfiguration(
        "eb-mvp01-20200325-00001", 100.0, scan_types, processing_blocks
    )

    sbd.sdp_configuration = sdp_configuration

    # Add dish_allocation
    dish_allocation = DishAllocation(receptor_ids=["0001", "0002"])
    sbd.dish_allocations = dish_allocation
    # Add dish_configurations
    dish_config = DishConfiguration(
        "dci_mvp01-20220329-00001", receiver_band=ReceiverBand.BAND_1
    )
    sbd.dish_configurations = [dish_config]

    return sbd


def create_test_low_sbdefinition():  # pylint: disable=too-many-locals
    """
    Utility method to create a valid LOW sb configuration for use in unit test
    """

    low_sbd = SBDefinition(
        sbd_id="sbi-mvp01-20200325-00001",
        telescope=TelescopeType.LOW,
        activities={
            "allocate": FilesystemScript(
                "/path/to/allocatescript.py",
                {
                    "init": PythonArguments(
                        args=["posarg1", "posarg2"], kwargs={"argname": "argval"}
                    ),
                    "main": PythonArguments(
                        args=["posarg1", "posarg2"], kwargs={"argname": "argval"}
                    ),
                },
            ),
            "observe": GitScript(
                repo="https://gitlab.com/script_repo/operational_scripts",
                path="/relative/path/to/scriptinsiderepo.py",
                branch="main",
                commit="d234c257dadd18b3edcd990b8194c6ad94fc278a",
                function_args={
                    "init": PythonArguments(
                        args=["posarg1", "posarg2"], kwargs={"argname": "argval"}
                    ),
                    "main": PythonArguments(
                        args=["posarg1", "posarg2"], kwargs={"argname": "argval"}
                    ),
                },
            ),
        },
    )

    low_sbd.metadata.created_on = datetime(
        2022, 3, 28, 15, 43, 53, 971548, tzinfo=timezone.utc
    )
    low_sbd.metadata.created_by = "Liz Bartlett"

    low_sbd.targets = [
        Target(
            target_id="target #1",
            pointing_pattern=PointingPattern(
                active=SinglePointParameters.kind, parameters=[SinglePointParameters()]
            ),
            reference_coordinate=HorizontalCoordinates(az=180.0, el=45.0),
        ),
        Target(
            target_id="target #2",
            pointing_pattern=PointingPattern(
                active=SinglePointParameters.kind, parameters=[SinglePointParameters()]
            ),
            reference_coordinate=HorizontalCoordinates(az=180.0, el=85.0),
        ),
    ]

    calibrator_scan = ScanDefinition(
        scan_definition_id="sbi-mvp01-20220328-00001",
        scan_duration=timedelta(seconds=64.0),
        target_id="target #1",
        target_beam_configuration_ids=["target #1 with beam A config 1"],
    )

    science_scan = ScanDefinition(
        scan_definition_id="sbi-mvp01-20220328-00002",
        scan_duration=timedelta(seconds=64.0),
        target_id="target #2",
        target_beam_configuration_ids=["target #2 with beam A config 1"],
    )

    low_sbd.scan_definitions = [calibrator_scan, science_scan]

    low_sbd.scan_sequence = [
        calibrator_scan.scan_definition_id,
        science_scan.scan_definition_id,
        science_scan.scan_definition_id,
        calibrator_scan.scan_definition_id,
    ]
    low_sbd.mccs_allocation = MCCSAllocation(
        subarray_beam_ids=["beam A"], station_ids=[[1, 2]], channel_blocks=[1]
    )

    low_sbd.target_beam_configurations = [
        TargetBeamConfiguration(
            target_beam_id="target #1 with beam A config 1",
            target="target #1",
            subarray_beam_configuration="beam A config 1",
        ),
        TargetBeamConfiguration(
            target_beam_id="target #2 with beam A config 1",
            target="target #2",
            subarray_beam_configuration="beam A config 1",
        ),
    ]

    subarray_beam_configurations = SubarrayBeamConfiguration(
        subarray_beam_configuration_id="beam A config 1",
        subarray_beam_id="beam A",
        update_rate=0.0,
        antenna_weights=[1.0, 1.0, 1.0],
        phase_centre=[0.0, 0.0],
        channels=[[0, 8, 1, 1], [8, 8, 2, 1]],
    )
    low_sbd.subarray_beam_configurations = [subarray_beam_configurations]

    return low_sbd


def load_string_from_file(filename):
    """
    Return a file from the current directory as a string
    """
    cwd, _ = os.path.split(__file__)
    path = os.path.join(cwd, filename)
    with open(path, "r", encoding="utf-8") as json_file:
        json_data = json_file.read()
        return json_data


VALID_MID_SBDEFINITION_JSON = load_string_from_file("testfile_sample_mid_sb.json")

VALID_LOW_SBDEFINITION_JSON = load_string_from_file("testfile_sample_low_sb.json")


def test_marshall_mid_sb_definition_to_json():
    """
    Verify that SBDefinition is marshalled to JSON correctly.
    """
    sbd = create_test_mid_sbdefinition()
    copy_sbd = deepcopy(sbd)
    expected = VALID_MID_SBDEFINITION_JSON
    json_str = SBDefinitionSchema().dumps(sbd)
    assert_json_is_equal(json_str, expected)

    # This ensures the first dump does not mutate any fields on the original object
    assert sbd == copy_sbd
    second_json_str = SBDefinitionSchema().dumps(sbd)
    assert_json_is_equal(second_json_str, expected)


def test_unmarshall_mid_sbdefinition_from_json():
    """
    Verify that SBDefinition is unmarshalled from JSON correctly.
    """
    expected = create_test_mid_sbdefinition()
    unmarshalled = SBDefinitionSchema().loads(VALID_MID_SBDEFINITION_JSON)
    assert unmarshalled == expected


def test_marshall_low_sb_definition_to_json():
    """
    Verify that SBDefinition is marshalled to JSON correctly.
    """
    sbd = create_test_low_sbdefinition()
    expected = VALID_LOW_SBDEFINITION_JSON
    json_str = SBDefinitionSchema().dumps(sbd)
    assert_json_is_equal(json_str, expected)


def test_unmarshall_low_sbdefinition_from_json():
    """
    Verify that SBDefinition is unmarshalled from JSON correctly.
    """
    expected = create_test_low_sbdefinition()
    unmarshalled = SBDefinitionSchema().loads(VALID_LOW_SBDEFINITION_JSON)
    assert unmarshalled == expected


def test_unmarshall_empty_sb():
    """
    Verify that an SBDefinition instance can be unmarshalled from JSON whose
    empty/null fields have been pruned.

    At the time of writing, we have just introduced the OpenAPI spec for the
    SBDefinition and need interoperability between the generated model and the
    PDM, at least until the PDM is deprecated. This test is required because
    empty fields are stripped from the OpenAPI model JSON, and we want to be
    sure that this JSON can be safely converted to a PDM instance and has the
    expected values.
    """
    new_sb_json = """{
  "activities": {},
  "interface": "https://schema.skao.int/ska-oso-pdm-sbd/0.1",
  "metadata": {
    "created_by": "DefaultUser",
    "created_on": "2022-07-28T08:39:19.287819",
    "last_modified_by": "DefaultUser",
    "last_modified_on": "2022-07-28T08:39:19.287819",
    "version": 1
  },
  "sbd_id": "sbd-t0001-20220728-00004",
  "telescope": "ska_mid"
}
"""

    timestamp = datetime.fromisoformat("2022-07-28T08:39:19.287819")

    expected = SBDefinition(
        sbd_id="sbd-t0001-20220728-00004",
        telescope=TelescopeType.MID,
        metadata=MetaData(
            created_by="DefaultUser",
            created_on=timestamp,
            last_modified_by="DefaultUser",
            last_modified_on=timestamp,
        ),
    )

    unmarshalled = SBDefinitionSchema().loads(new_sb_json)
    assert unmarshalled == expected
