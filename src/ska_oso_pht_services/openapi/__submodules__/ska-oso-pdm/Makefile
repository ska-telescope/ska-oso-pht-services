#
# CAR_OCI_REGISTRY_HOST, CAR_OCI_REGISTRY_USERNAME and PROJECT_NAME are combined to define
# the Docker tag for this project. The definition below inherits the standard
# value for CAR_OCI_REGISTRY_HOST (=artefact.skao.int) and overwrites
# PROJECT to give a final Docker tag of artefact.skao.int/ska-oso-pdm
#
CAR_OCI_REGISTRY_HOST ?= artefact.skao.int
CAR_OCI_REGISTRY_USERNAME ?= ska-telescope
PROJECT_NAME = ska-oso-pdm

OCI_IMAGE_BUILD_CONTEXT = $(PWD)

# include makefile to pick up the standard Make targets from the submodule
-include .make/base.mk
-include .make/python.mk
-include .make/oci.mk

# include your own private variables for custom deployment configuration
-include PrivateRules.mak

# Unset Black and isort configs so that definitions in pyproject.toml take effect
PYTHON_SWITCHES_FOR_BLACK =
PYTHON_SWITCHES_FOR_ISORT =

diagrams:  ## recreate PlantUML diagrams whose source has been modified
	@for i in $$(git diff --name-only -- '*.puml'); \
	do \
		echo "Recreating $${i%%.*}.png"; \
		cat $$i | docker run --rm -i think/plantuml -tpng $$i > $${i%%.*}.png; \
	done

# MINIKUBE_NFS_SHARE_PATH is appended to the volume mounted during code generation.
# Developers can redefine this value to match their Minikube NFS share setup,
# which will allow the codegen For instance, a Mac where SKA minikube is installed
# with a command like
#
#    make RUNTIME=docker --nfs-share=$HOME --nfs-shares-root=/nfsshares minikube-install
#
# the $HOME directory would be mounted at /nfsshares, so MINIKUBE_NFS_SHARE_PATH should
# also be set to /nfsshares
MINIKUBE_NFS_SHARES_ROOT ?=

# openapi-generator-cli and swagger-cli have a bug where you can't specify
# multiple supportingFiles, so we need n calls for n generated output groups
CODEGEN_TARGETS = models \
      supportingFiles=encoder.py \
      supportingFiles=base_model_.py \
      supportingFiles=typing_utils.py \
      supportingFiles=util.py

models:
	$(foreach var,$(CODEGEN_TARGETS),$(OCI_BUILDER)run --rm --volume "$(MINIKUBE_NFS_SHARES_ROOT)$(PWD):/local" openapitools/openapi-generator-cli \
		generate \
		-i /local/src/ska_oso_pdm/openapi/oso-components-openapi-v1.yaml \
		-g python-flask \
		-o /local/src \
		--package-name ska_oso_pdm.generated \
		--global-property "$(var),generateSourceCodeOnly=true" ;)

unified:
	$(OCI_BUILDER)run --rm --volume "$(MINIKUBE_NFS_SHARES_ROOT)$(PWD):/local" openapitools/openapi-generator-cli \
    	generate \
		-i /local/src/ska_oso_pdm/openapi/oso-components-openapi-v1.yaml \
    	-g openapi-yaml \
		-o /local/openapi \
		--additional-properties outputFile=/local/openapi/unified.yaml
