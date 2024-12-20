Changelog
==========

All notable changes to this project will be documented in this file.
This project adheres to [Semantic Versioning](http://semver.org/).

Unreleased
*****

2.4.1

*****
* Updates to ska-db-oda ^6.3.1

2.4.0

*****

* Tagging as a minor release due to the issues with 2.3.0 tag not having correct changelog
* [BREAKING] Updates to ska-db-oda ^6.2.1 from 5.2.0. This is a breaking change as it is also using PDM objects in the request bodies of the API. See ODA change log for details on model and table changes.
* Updated the dependencies. PDM is now inferred from ODA, not referenced directly.
* Updated to use  UnitOfWork from ODA 


2.3.1

*****

* Released the previous version due to the tag 2.3.0 already been pushed with incorrect changelog

2.3.0
*****

* Add send-email endpoint 

2.2.0

*****

* Refactored validate endpoint

2.1.0

*****

* Add delete signed URL endpoint
* Update makefile for pgadmin4 local testing

2.0.1

*****

* Fix API path `v2`


2.0.0

*****

* [BREAKING] Updates to ska-oso-pdm ^14.3.0 from ^11.3.0. This is a breaking change as the PDM objects are the request bodies of the PHT services API. See PDM change log for details on model changes.
* [BREAKING] Updates to ska-db-oda ^5.2.0 from 2.1.6. This is a breaking change as it is also using PDM objects in the request bodies of the API. See ODA change log for details on model and table changes.
* Dockerfile to use image ska-cicd-k8s-tools-build-deploy:0.12.0
* ci image to use $SKA_K8S_TOOLS_BUILD_DEPLOY