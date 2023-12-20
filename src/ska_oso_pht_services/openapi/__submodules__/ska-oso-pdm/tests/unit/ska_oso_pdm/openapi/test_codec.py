from datetime import datetime

from ska_oso_pdm.generated.models.author import Author
from ska_oso_pdm.generated.models.execution_block import ExecutionBlock
from ska_oso_pdm.generated.models.metadata import Metadata
from ska_oso_pdm.generated.models.observing_programme import ObservingProgramme
from ska_oso_pdm.generated.models.project import Project
from ska_oso_pdm.generated.models.python_arguments import PythonArguments
from ska_oso_pdm.generated.models.sb_definition import SBDefinition
from ska_oso_pdm.generated.models.sb_instance import SBInstance
from ska_oso_pdm.generated.models.telescope import Telescope
from ska_oso_pdm.openapi import CODEC
from tests.unit.ska_oso_pdm.utils import assert_json_is_equal

from .util import (
    EXECUTION_BLOCK_JSON,
    LOW_SBD_JSON,
    MID_SBD_JSON,
    PROJECT_JSON,
    SB_INSTANCE_JSON,
)

SAMPLE_DATETIME = datetime.fromisoformat("2022-09-23T15:43:53.971548+00:00")

metadata = Metadata(
    version=1,
    created_by="TestUser",
    created_on=SAMPLE_DATETIME,
    last_modified_by="TestUser",
    last_modified_on=SAMPLE_DATETIME,
)

scheduling_block_instance = SBInstance(
    metadata=metadata,
    interface="https://schema.skao.int/ska-oso-pdm-sbi/0.1",
    sbi_id="sbi-mvp01-20220923-00001",
    telescope=Telescope.SKA_MID,
    sbd_id="sbd-mvp01-20220923-00001",
    sbd_version=1,
    executed_on=SAMPLE_DATETIME,
    subarray_id=3,
    runtime_args=PythonArguments(),
)

execution_block = ExecutionBlock(
    metadata=metadata,
    interface="https://schema.skao.int/ska-oso-pdm-eb/0.1",
    eb_id="eb-mvp01-20220923-00001",
    telescope=Telescope.SKA_MID,
    sbd_id="sbd-mvp01-20220923-00001",
    sbd_version=1,
)

project = Project(
    metadata=metadata,
    interface="https://schema.skao.int/ska-oso-pdm-prj/0.1",
    prj_id="prj-mvp01-20220923-00001",
    telescope=Telescope.SKA_MID,
    author=Author(["John Lennon"], ["Ringo Starr", "George Harrison"]),
    obs_programmes=[
        ObservingProgramme(
            name="Programme 1",
            sbd_ids=[
                "sbd-mvp01-20220923-00001",
                "sbd-mvp01-20220923-00002",
                "sbd-mvp01-20220923-00003",
            ],
        ),
        ObservingProgramme(
            name="Programme 2",
            sbd_ids=[
                "sbd-mvp01-20220923-00004",
                "sbd-mvp01-20220923-00005",
                "sbd-mvp01-20220923-00006",
            ],
        ),
    ],
)


def test_sbi_from_json():
    result = CODEC.loads(SBInstance, SB_INSTANCE_JSON)
    assert result == scheduling_block_instance


def test_sbi_to_json():
    result = CODEC.dumps(scheduling_block_instance)
    assert_json_is_equal(result, SB_INSTANCE_JSON)


def test_eb_from_json():
    result = CODEC.loads(ExecutionBlock, EXECUTION_BLOCK_JSON)
    assert result == execution_block


def test_eb_to_json():
    result = CODEC.dumps(execution_block)
    assert_json_is_equal(result, EXECUTION_BLOCK_JSON)


def test_prj_from_json():
    result = CODEC.loads(Project, PROJECT_JSON)
    assert result == project


def test_prj_to_json():
    result = CODEC.dumps(project)
    assert_json_is_equal(result, PROJECT_JSON)


def test_mid_round_trip():
    marshalled = CODEC.dumps(CODEC.loads(SBDefinition, MID_SBD_JSON))
    assert_json_is_equal(marshalled, MID_SBD_JSON)


def test_low_round_trip():
    marshalled = CODEC.dumps(CODEC.loads(SBDefinition, LOW_SBD_JSON))
    assert_json_is_equal(marshalled, LOW_SBD_JSON)
