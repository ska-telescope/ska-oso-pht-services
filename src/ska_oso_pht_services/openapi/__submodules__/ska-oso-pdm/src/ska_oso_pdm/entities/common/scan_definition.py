"""
The entities.scan_definition_entity module defines
simple Python representation of a single observation scan
"""

__all__ = ["ScanDefinition", "ScanDefinitionID"]

import uuid
from datetime import timedelta
from typing import List, Optional

from ska_oso_pdm.entities.common import ScanDefinitionID
from ska_oso_pdm.entities.csp.common import CSPConfigurationID
from ska_oso_pdm.entities.dish.dish_configuration import DishConfigurationID
from ska_oso_pdm.entities.mccs.target_beam_configuration import (
    TargetBeamConfigurationID,
)
from ska_oso_pdm.entities.sdp import ScanTypeID


class ScanDefinition:
    """
    ScanDefinition represents the instrument configuration for a single scan.
    """

    def __init__(
        self,
        *,  # force kw-only args
        scan_definition_id: Optional[ScanDefinitionID],
        scan_duration: timedelta,
        target_id: Optional[str] = None,
        target_beam_configuration_ids: Optional[List[TargetBeamConfigurationID]] = None,
        dish_configuration_id: Optional[DishConfigurationID] = None,
        scan_type_id: Optional[ScanTypeID] = None,
        csp_configuration_id: Optional[CSPConfigurationID] = None,
    ):  # pylint: disable=invalid-name too-many-arguments

        """
        Return a new ScanDefinition object.

        :param scan_definition_id: the unique ID for this scan definition
        :param scan_duration: scan duration
        :target_id: ID of target to observe
        :target_beam_configurations: SKA LOW sub-array beam configurations to apply
        during this scan.
        :dish_configuration_id: SKA MID dish configuration ID during this scan.
        :scan_type_id: SKA MID scan type ID
        :csp_configuration_id: SKA MID  Central Signal Processor ID
        """
        if scan_definition_id is None:
            scan_definition_id = uuid.uuid4()
        self.scan_definition_id = scan_definition_id

        self.scan_duration = scan_duration
        self.target_id = target_id
        self.target_beam_configuration_ids = target_beam_configuration_ids
        self.scan_type_id = scan_type_id
        self.csp_configuration_id = csp_configuration_id
        self.dish_configuration_id = dish_configuration_id

    def __eq__(self, other):
        if not isinstance(other, ScanDefinition):
            return False

        return (
            self.scan_definition_id == other.scan_definition_id
            and self.scan_duration == other.scan_duration
            and self.target_id == other.target_id
            and self.target_beam_configuration_ids
            == other.target_beam_configuration_ids
            and self.scan_type_id == other.scan_type_id
            and self.dish_configuration_id == other.dish_configuration_id
            and self.csp_configuration_id == other.csp_configuration_id
        )

    def __repr__(self):
        return (
            f"<ScanDefinition(scan_definition_id={self.scan_definition_id!r}, "
            f"scan_duration={self.scan_duration}, "
            f"target_id={self.target_id}, "
            f"target_beam_configuration_ids={self.target_beam_configuration_ids}, "
            f"scan_type_id={self.scan_type_id}, "
            f"dish_configuration_id={self.dish_configuration_id}, "
            f"csp_configuration_id={self.csp_configuration_id})>"
        )
