#
# CAR_OCI_REGISTRY_HOST, CAR_OCI_REGISTRY_USERNAME and PROJECT_NAME are combined to define
# the Docker tag for this project. The definition below inherits the standard
# value for CAR_OCI_REGISTRY_HOST (=artefact.skao.int) and overwrites
# PROJECT_NAME to give a final Docker tag of artefact.skao.int/ska-oso-pht-services
#
CAR_OCI_REGISTRY_HOST ?= artefact.skao.int
CAR_OCI_REGISTRY_USERNAME ?= ska-telescope
PROJECT_NAME = ska-oso-pht-services
KUBE_NAMESPACE ?= ska-oso-pht-services
CLUSTER_DOMAIN ?= cluster.local
RELEASE_NAME ?= test

AWS_PHT_BUCKET_NAME ?=
AWS_SERVER_PUBLIC_KEY ?=
AWS_SERVER_SECRET_KEY ?=
SMTP_PASSWORD ?=

# Set sphinx documentation build to fail on warnings (as it is configured
# in .readthedocs.yaml as well)
DOCS_SPHINXOPTS ?= -W --keep-going

IMAGE_TO_TEST = $(CAR_OCI_REGISTRY_HOST)/$(strip $(OCI_IMAGE)):$(VERSION)
K8S_CHART = ska-oso-pht-services-umbrella

POSTGRES_HOST ?= $(RELEASE_NAME)-postgresql
K8S_CHART_PARAMS += \
  --set ska-db-oda-umbrella.pgadmin4.serverDefinitions.servers.firstServer.Host=$(POSTGRES_HOST)

# For the test, dev and integration environment, use the freshly built image in the GitLab registry
ENV_CHECK := $(shell echo $(CI_ENVIRONMENT_SLUG) | egrep 'test|dev|integration')
ifneq ($(ENV_CHECK),)
K8S_CHART_PARAMS = --set ska-oso-pht-services.rest.image.tag=$(VERSION)-dev.c$(CI_COMMIT_SHORT_SHA) \
	--set ska-oso-pht-services.rest.image.registry=$(CI_REGISTRY)/ska-telescope/oso/ska-oso-pht-services
endif

K8S_CHART_PARAMS += \
	--set global.cluster_domain=$(CLUSTER_DOMAIN)

# For the staging environment, make k8s-install-chart-car will pull the chart from CAR so we do not need to
# change any values
ENV_CHECK := $(shell echo $(CI_ENVIRONMENT_SLUG) | egrep 'staging')
ifneq ($(ENV_CHECK),)
endif

# unset defaults so settings in pyproject.toml take effect
PYTHON_SWITCHES_FOR_BLACK = --extend-exclude "(src/ska_oso_pht_services/generated|src/ska_oso_pht_services/openapi/__submodules__)"
PYTHON_SWITCHES_FOR_ISORT =
PYTHON_SWITCHES_FOR_PYLINT =

# Restore Black's preferred line length which otherwise would be overridden by
# System Team makefiles' 79 character default
PYTHON_LINE_LENGTH = 88

# Set the k8s test command run inside the testing pod to only run the component
# tests (no k8s pod deployment required for unit tests)
K8S_TEST_TEST_COMMAND = KUBE_NAMESPACE=$(KUBE_NAMESPACE) pytest ./tests/component | tee pytest.stdout

# Set python-test make target to run unit tests and not the component tests
PYTHON_TEST_FILE = tests/unit/

# include makefile to pick up the standard Make targets from the submodule
-include .make/base.mk
-include .make/python.mk
-include .make/oci.mk
-include .make/k8s.mk

-include .make/helm.mk

# include your own private variables for custom deployment configuration
-include PrivateRules.mak

REST_POD_NAME=$(shell kubectl get pods -o name -n $(KUBE_NAMESPACE) -l app=ska-oso-pht-services,component=rest | cut -c 5-)

$(info    KUBE_NAMESPACE is $(KUBE_NAMESPACE))
$(info    REST_POD_NAME is $(REST_POD_NAME))

# install helm plugin from https://github.com/helm-unittest/helm-unittest.git
# k8s-chart-test:
# 	mkdir -p charts/build; \
# 	helm unittest charts/ska-oso-odt-services/ --with-subchart \
# 		--output-type JUnit --output-file charts/build/chart_template_tests.xml

k8s-pre-test:	
	kubectl exec $(REST_POD_NAME) -n $(KUBE_NAMESPACE) -- mkdir -p /var/lib/oda/prsl/prsl-1234
	kubectl cp tests/unit/testfile_sample_proposal.json $(KUBE_NAMESPACE)/$(REST_POD_NAME):/var/lib/oda/prsl/prsl-1234/1.json

k8s-post-test:
	# kubectl -n $(KUBE_NAMESPACE) exec $(REST_POD_NAME) -- rm -r /var/lib/oda/prsl/

MINIKUBE_NFS_SHARES_ROOT ?=

# openapi-generator-cli and swagger-cli have a bug where you can't specify
# multiple supportingFiles, so we need n calls for n generated output groups
CODEGEN_TARGETS = models \
	supportingFiles=encoder.py \
	supportingFiles=base_model_.py \
	supportingFiles=typing_utils.py \
	supportingFiles=util.py


models:  ## generate models from OpenAPI spec
	$(foreach var,$(CODEGEN_TARGETS),$(OCI_BUILDER)run --rm --volume "$(MINIKUBE_NFS_SHARES_ROOT)$(PWD):/local" openapitools/openapi-generator-cli \
		generate \
		-i /local/src/ska_oso_pht_services/openapi/pht-openapi-v1.yaml \
		-g python-flask \
		-o /local/src \
		--package-name ska_oso_pht_services.generated \
		--global-property "$(var),generateSourceCodeOnly=true" ;)

#models: ## generate models from OpenAPI spec
#	docker run --rm --volume "$(PWD):/local" swaggerapi/swagger-codegen-cli-v3 generate \
#		-i /local/src/ska_oso_pht_services/swagger/pht-openapi-v1.yaml \
#		-l python-flask \
#		-c /local/codegen-conf.json \
#		-o /local/src/ska_oso_pht_services \
#		-Dmodels --model-package=models
#	find ./src/ska_oso_pht_services/generated/models/*.py -exec sed -i "" 's/from generated/from ska_oso_pht_services.generated/' {} +

dev-up: K8S_CHART_PARAMS = \
	--set ska-oso-pht-services.rest.image.tag=$(VERSION) \
	--set ska-oso-pht-services.rest.ingress.enabled=true \
	--set ska-oso-pht-services.secretProvider.enabled=false \
	--set global.minikube=true \
	--set global.env.aws_pht_bucket_name=$(AWS_PHT_BUCKET_NAME) \
	--set global.env.aws_server_public_key=$(AWS_SERVER_PUBLIC_KEY) \
	--set global.env.aws_server_secret_key=$(AWS_SERVER_SECRET_KEY) \
	--set global.env.smtp_password='$(SMTP_PASSWORD)' \
	--set global.cluster_domain=cluster.local \
	--set ska-db-oda-umbrella.pgadmin4.serverDefinitions.servers.firstServer.Host=$(POSTGRES_HOST)

dev-up: k8s-namespace k8s-install-chart k8s-wait ## bring up developer deployment

dev-down: k8s-uninstall-chart k8s-delete-namespace  ## tear down developer deployment
