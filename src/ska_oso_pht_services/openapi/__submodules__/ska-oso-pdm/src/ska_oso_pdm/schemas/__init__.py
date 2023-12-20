"""
The  schemas for the SKA Project Data Model (PDM).
"""
__all__ = ["CODEC"]

from .codec import MarshmallowCodec

CODEC = MarshmallowCodec()

# this is intentional because CODEC has to be defined before these are included
# pylint: disable=wrong-import-position cyclic-import wrong-import-order

from ska_oso_pdm.schemas.common.sb_definition import (  # noqa F401 E402
    SBDefinitionSchema,
)
from ska_oso_pdm.schemas.common.scan_definition import (  # noqa F401 E402
    ScanDefinitionSchema,
)
from ska_oso_pdm.schemas.csp.common import CSPConfigurationSchema  # noqa F401 E402
from ska_oso_pdm.schemas.mccs.mccs_allocation import (  # noqa F401 E402
    MCCSAllocationSchema,
)
from ska_oso_pdm.schemas.mccs.subarray_beam_configuration import (  # noqa F401 E402
    SubarrayBeamConfigurationSchema,
)
from ska_oso_pdm.schemas.mccs.target_beam_configuration import (  # noqa F401 E402
    TargetBeamConfigurationSchema,
)

from .common.sb_definition import SBDefinitionSchema  # noqa F401 E402
from .common.scan_definition import ScanDefinitionSchema  # noqa F401 E402
