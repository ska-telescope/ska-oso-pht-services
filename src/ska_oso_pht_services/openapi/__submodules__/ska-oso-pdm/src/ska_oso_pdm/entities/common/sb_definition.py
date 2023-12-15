"""
The entities.scheduling_block_entity module defines
a simple Python representation of the scheduling block
that contains the details of the observation
"""
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Dict, List, Optional

from ska_oso_pdm.entities.common import SBDefinitionID
from ska_oso_pdm.entities.common.procedures import PythonProcedure
from ska_oso_pdm.entities.common.scan_definition import ScanDefinition, ScanDefinitionID
from ska_oso_pdm.entities.common.target import Target
from ska_oso_pdm.entities.csp.common import CSPConfiguration
from ska_oso_pdm.entities.dish.dish_allocation import DishAllocation
from ska_oso_pdm.entities.dish.dish_configuration import DishConfiguration
from ska_oso_pdm.entities.mccs.mccs_allocation import MCCSAllocation
from ska_oso_pdm.entities.mccs.subarray_beam_configuration import (
    SubarrayBeamConfiguration,
)
from ska_oso_pdm.entities.mccs.target_beam_configuration import TargetBeamConfiguration
from ska_oso_pdm.entities.sdp.sdp_configuration import SDPConfiguration

__all__ = ["SBDefinition", "TelescopeType", "MetaData"]

# URI of the Scheduling Block definition. Not currently part of telescope model.
SBD_SCHEMA_URI = "https://schema.skao.int/ska-oso-pdm-sbd/0.1"


class TelescopeType(Enum):
    """
    TelescopeType represents which telescope is being used
    """

    MID = "ska_mid"
    LOW = "ska_low"
    MEERKAT = "MeerKAT"


class MetaData:
    """
    MetaData Class
    """

    def __init__(
        self,
        *,
        version: Optional[int] = 1,
        created_on: Optional[datetime] = None,
        created_by: Optional[str] = None,
        last_modified_on: Optional[datetime] = None,
        last_modified_by: Optional[str] = None,
    ):
        self.version = version

        if created_on is None:
            created_on = datetime.now(timezone.utc)
        self.created_on = created_on

        self.created_by = created_by

        self.last_modified_on = last_modified_on

        self.last_modified_by = last_modified_by

    def __eq__(self, other):
        if not isinstance(other, MetaData):
            return False

        return (
            self.version == other.version
            and self.created_on == other.created_on
            and self.created_by == other.created_by
            and self.last_modified_on == other.last_modified_on
            and self.last_modified_by == other.last_modified_by
        )

    def __repr__(self):
        return (
            f"<MetaData("
            f"version={self.version}, "
            f"created_on={self.created_on}, "
            f"created_by={self.created_by}, "
            f"last_modified_on={self.last_modified_on}, "
            f"last_modified_by={self.last_modified_by})>"
        )


class SBDefinition:  # pylint: disable=too-few-public-methods too-many-instance-attributes
    """
    SKA scheduling block
    """

    def __init__(
        self,
        *,  # force kw-only args
        interface: Optional[str] = SBD_SCHEMA_URI,
        sbd_id: Optional[SBDefinitionID] = None,
        telescope: Optional[TelescopeType] = None,
        metadata: Optional[MetaData] = None,
        activities: Optional[Dict[str, PythonProcedure]] = None,
        targets: Optional[List[Target]] = None,
        scan_definitions: Optional[List[ScanDefinition]] = None,
        scan_sequence: Optional[List[ScanDefinitionID]] = None,
        sdp_configuration: Optional[SDPConfiguration] = None,
        dish_configurations: Optional[List[DishConfiguration]] = None,
        csp_configurations: Optional[List[CSPConfiguration]] = None,
        dish_allocations: Optional[DishAllocation] = None,
        mccs_allocation: Optional[MCCSAllocation] = None,
        subarray_beam_configurations: Optional[List[SubarrayBeamConfiguration]] = None,
        target_beam_configurations: Optional[List[TargetBeamConfiguration]] = None,
    ):  # pylint: disable=too-many-arguments too-many-locals

        self.interface = interface
        self.telescope = telescope

        if metadata is None:
            metadata = MetaData()
        self.metadata = metadata

        self.activities: Dict[str, PythonProcedure] = {}
        if activities:
            self.activities.update(activities)

        if sbd_id is None:
            sbd_id = str(uuid.uuid4())
        self.sbd_id = sbd_id

        self.targets: List[Target] = []
        if targets:
            self.targets.extend(targets)

        self.scan_definitions: List[ScanDefinition] = []
        if scan_definitions:
            self.scan_definitions.extend(scan_definitions)

        self.scan_sequence: List[ScanDefinitionID] = []
        if scan_sequence:
            self.scan_sequence.extend(scan_sequence)

        self.dish_configurations: List[DishConfiguration] = []
        if dish_configurations:
            self.dish_configurations.extend(dish_configurations)

        self.csp_configurations: List[CSPConfiguration] = []
        if csp_configurations:
            self.csp_configurations.extend(csp_configurations)

        self.sdp_configuration = sdp_configuration

        self.dish_allocations = dish_allocations

        self.mccs_allocation = mccs_allocation

        self.subarray_beam_configurations: List[SubarrayBeamConfiguration] = []
        if subarray_beam_configurations:
            self.subarray_beam_configurations.extend(subarray_beam_configurations)

        self.target_beam_configurations: List[TargetBeamConfiguration] = []
        if target_beam_configurations:
            self.target_beam_configurations.extend(target_beam_configurations)

    def __eq__(self, other):
        if not isinstance(other, SBDefinition):
            return False

        return (
            self.sbd_id == other.sbd_id
            and self.interface == other.interface
            and self.telescope == other.telescope
            and self.metadata == other.metadata
            and self.activities == other.activities
            and self.targets == other.targets
            and self.scan_definitions == other.scan_definitions
            and self.scan_sequence == other.scan_sequence
            and self.sdp_configuration == other.sdp_configuration
            and self.dish_configurations == other.dish_configurations
            and self.csp_configurations == other.csp_configurations
            and self.dish_allocations == other.dish_allocations
            and self.mccs_allocation == other.mccs_allocation
            and self.subarray_beam_configurations == other.subarray_beam_configurations
            and self.target_beam_configurations == other.target_beam_configurations
        )

    def __repr__(self):
        return (
            f"<SBDefinition("
            f"id={self.sbd_id}, "
            f"interface={self.interface}, "
            f"telescope={self.telescope}, "
            f"metadata={self.metadata}, "
            f"activities={self.activities}, "
            f"targets={self.targets}, "
            f"scan_defs={self.scan_definitions}, "
            f"scan_sequence={self.scan_sequence}, "
            f"sdp={self.sdp_configuration}, "
            f"dish_configs={self.dish_configurations}, "
            f"csp={self.csp_configurations}, "
            f"dish_allocation={self.dish_allocations}, "
            f"mccs_allocation={self.mccs_allocation}, "
            f"subarray_beam_configurations={self.subarray_beam_configurations}, "
            f"target_beam_configurations={self.target_beam_configurations})>"
        )
