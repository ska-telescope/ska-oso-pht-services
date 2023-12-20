"""
Unit tests for the ska_oso_pdm.entities.sb_definition module.
"""
import copy
from datetime import datetime, timedelta, timezone

import pytest

from ska_oso_pdm.entities.common.sb_definition import (
    SBD_SCHEMA_URI,
    MetaData,
    SBDefinition,
    TelescopeType,
)


def test_sb_definitions_defaults():
    """
    Verify SBDefinition default arguments are equal.
    """
    # Create shared metadata to avoid different datetime.now() comparisons
    metadata = MetaData()
    sbd_1 = SBDefinition(sbd_id="sbd1", metadata=metadata)
    sbd_2 = SBDefinition(sbd_id="sbd1", metadata=metadata)
    assert sbd_1 == sbd_2


def test_sb_definitions_object_equality():
    """
    Verify SBDefinition objects are not equal when SBI ID is different.
    """
    sbd_1 = SBDefinition()
    sbd_2 = copy.deepcopy(sbd_1)
    sbd_2.sbd_id = "abc"

    assert sbd_2 != sbd_1


def test_sb_definition_interface_is_defined():
    """
    Verify that the SBDefinition interface value is set.
    """
    sbd = SBDefinition()
    assert sbd.interface == SBD_SCHEMA_URI


def test_telescope_type_is_set_correctly():
    """
    Verify that telescope type is set correctly
    """
    assert TelescopeType.LOW.value == "ska_low"
    assert TelescopeType.MID.value == "ska_mid"
    assert TelescopeType.MEERKAT.value == "MeerKAT"


def test_telescope_type_is_set_within_sb():
    """
    Verify that the telescope type is set correctly within an sb
    """
    sbd = SBDefinition(telescope=TelescopeType.MID)
    assert sbd.telescope.value == "ska_mid"


def test_metadata():
    """
    Test a MetaData Object is created correctly and has a correct timestamp
    """
    delta = timedelta(seconds=1)
    metadata = MetaData()

    assert metadata.created_on.timestamp() == pytest.approx(
        datetime.now(timezone.utc).timestamp(), abs=delta.total_seconds()
    )

    assert metadata.version == 1


def test_metadata_within_an_sb():
    """
    Test a MetaData Object is generated when an sb is created
    """

    sbd = SBDefinition()
    author = "Liz Bartlett"
    sbd.metadata.created_by = author

    assert sbd.metadata.created_by == author
    assert sbd.metadata.version == 1
