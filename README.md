Proposal Handling Tool Services
================================

# Quick start
To clone this repository, run

```
git clone --recurse-submodules git@gitlab.com:ska-telescope/oso/ska-oso-pht-services.git
```

To refresh the GitLab Submodule, execute below commands:

```
git submodule update --recursive --remote
git submodule update --init --recursive
```

### Build and test

Install dependencies with Poetry and activate the virtual environment

```
poetry install
poetry shell
```

To build a new Docker image for the PHT, run

```
make oci-build
```

Execute the test suite and lint the project with:

```
make python-test
make python-lint
```

### Deploy to local Kubernetes for development
Export secrets locally
```
export AWS_PHT_BUCKET_NAME=<AWS Bucket Name>
export AWS_SERVER_PUBLIC_KEY=<AWS Public Key>
export AWS_SERVER_SECRET_KEY=<AWS Secret Key>
export AWS_REGION_NAME=<AWS Region Name>
```

Install the Helm umbrella chart into a Kubernetes cluster with ingress enabled:

```
make dev-up
```

The Swagger UI should be available external to the cluster at `http://<KUBE_HOST>/<KUBE_NAMESPACE>/pht/api/v1/ui/` and the API accesible via the same URL.

If using minikube, `KUBE_HOST` can be found by running `minikube ip`. 
`KUBE_NAMESPACE` is the namespace the chart was deployed to, likely `ska-oso-pht-services`

To run the component tests in a k8s pod:

```
make k8s-test
```

To uninstall the chart, run

```
make dev-down
```

# Documentation

[![Documentation Status](https://readthedocs.org/projects/ska-telescope-ska-oso-pht-services/badge/?version=latest)](https://developer.skao.int/projects/ska-oso-pht-services/en/latest/?badge=latest)

Documentation can be found in the ``docs`` folder. To build docs, install the
documentation specific requirements:

```
pip3 install sphinx sphinx-rtd-theme recommonmark sphinxcontrib-openapi mistune==0.8.4
```

and build the documentation (will be built in docs/build folder) with

```
make docs-build html
```
