# SKA Project Data Model library

The repository for the Data Model library

## Project Description

This project contains the code for the Project Data Model. The Project Data Model defines a high-level view of the information held for an observation on one of the SKA Telescopes. The code is used by the Observation Execution Tool the application which provides high-level scripting facilities and a high-level scripting UI for the SKA.
Currently this code provides a limited Scheduling Block definition (scan and field info only).
The Scheduling Block is the basic unit of observing within the SKA containing enough information to run a single observation.

## Quickstart

This project is structured to use Docker containers for development and
testing so that the build environment, test environment and test results are
all completely reproducible and are independent of host environment. It uses
``make`` to provide a consistent UI.


Execute the test suite and lint the project with:

```
make python-test
make python-lint
```

To build a new Docker image for the PDM, run

```
make oci-build
```

## OpenAPI

The [OpenAPI component definitions](./src/ska_oso_pdm/openapi/) form the primary definitions of the entities used in the OSO services.
The Python models are generated from these definitions using [Swagger Codegen](https://swagger.io/tools/swagger-codegen/). 
There is a target in the Makefile which will generate the models based on the OpenAPI docs. To regenerate the models, run:
```
make models
```
## Documentation

[![Documentation Status](https://readthedocs.org/projects/ska-telescope-ska-oso-pdm/badge/?version=latest)](https://developer.skao.int/projects/ska-oso-pdm/en/latest/?badge=latest)

Documentation can be found in the ``docs`` folder. To build docs, install the
documentation specific requirements:

```
pip3 install sphinx sphinx-rtd-theme recommonmark
```

and build the documentation (will be built in docs/build folder) with

```
make docs-build html
```

