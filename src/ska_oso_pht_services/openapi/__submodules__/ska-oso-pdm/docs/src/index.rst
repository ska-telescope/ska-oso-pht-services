===========
ska-oso-pdm
===========

.. HOME SECTION ==================================================

.. Hidden toctree to manage the sidebar navigation.

.. toctree::
  :maxdepth: 1
  :caption: Table of Contents
  :hidden:

  quickstart
  background
  layout/layout
  json

.. COMMUNITY SECTION ==================================================

.. Hidden toctree to manage the sidebar navigation.

.. toctree::
  :maxdepth: 1
  :caption: API Documentation
  :hidden:

  api/entities/common/__init__
  api/entities/common/target
  api/entities/common/procedures
  api/entities/common/sb_definition
  api/entities/common/scan_definition
  api/entities/csp/common
  api/entities/sdp/sdp
  api/entities/dish/dish_allocation
  api/entities/dish/dish_configuration
  api/entities/mccs/mccs_allocation
  api/entities/mccs/subarray_beam_configuration
  api/entities/mccs/target_beam_configuration

  api/schemas/codec
  api/schemas/shared
  api/schemas/common/__init__
  api/schemas/common/target
  api/schemas/common/procedures
  api/schemas/common/sb_definition
  api/schemas/common/scan_definition
  api/schemas/csp/common
  api/schemas/sdp/sdp
  api/schemas/dish/dish_allocation
  api/schemas/dish/dish_configuration
  api/schemas/mccs/mccs_allocation
  api/schemas/mccs/subarray_beam_configuration
  api/schemas/mccs/target_beam_configuration

Project description
===================

The SKA Project Data Model (PDM) is the data model used for 'offline'
observatory processes. PDM entities such as observing proposals, observing
programmes, scheduling blocks, etc., capture all the information required to
describe and grade an observing proposal and any associated scheduling blocks.
ska-oso-pdm is a Python object model and JSON serialisation library for the
PDM.

Status
------

The SB definition evolves from PI to PI as more elements are added to the
system and greater element configuration space is exposed. Practically
speaking, this library should be considered the best reference for the current
state of SB design.

For examples of SBs, see the :ref:`MID JSON representation` and
:ref:`LOW JSON representation`.

Historical references can be found here:

- `PI3 MID SB <https://confluence.skatelescope.org/pages/viewpage.action?pageId=74731324>`__
- `PI6 MID SB <https://confluence.skatelescope.org/x/TAaKBg>`__
- `PI10 LOW SB <https://confluence.skatelescope.org/x/O4NDC>`__
- `PI11 MID SB <https://confluence.skatelescope.org/x/Cg6qC>`__
- `PI11 LOW SB <https://confluence.skatelescope.org/x/VRWqC>`__

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
