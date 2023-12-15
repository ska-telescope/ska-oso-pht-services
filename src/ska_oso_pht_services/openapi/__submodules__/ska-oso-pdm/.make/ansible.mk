# include Makefile for Ansible roles/collections related targets and variables

# do not declare targets if help had been invoked
ifneq (long-help,$(firstword $(MAKECMDGOALS)))
ifneq (help,$(firstword $(MAKECMDGOALS)))

ifeq ($(strip $(PROJECT)),)
  NAME=$(shell basename $(CURDIR))
else
  NAME=$(PROJECT)
endif

RELEASE_SUPPORT := $(shell dirname $(abspath $(lastword $(MAKEFILE_LIST))))/.make-release-support
ANSIBLE_SCRIPT_DIR := $(shell dirname $(abspath $(lastword $(MAKEFILE_LIST))))

VERSION=$(shell . $(RELEASE_SUPPORT) ; RELEASE_CONTEXT_DIR=$(RELEASE_CONTEXT_DIR) setContextHelper; getVersion)
TAG=$(shell . $(RELEASE_SUPPORT); RELEASE_CONTEXT_DIR=$(RELEASE_CONTEXT_DIR) setContextHelper; getTag)

SHELL=/usr/bin/env bash

.PHONY: ansible-pre-lint ansible-do-lint ansible-post-lint ansible-lint \
	ansible-publish ansible-pre-publish ansible-do-publish

ansible-pre-lint:

ansible-post-lint:

ansible-do-lint: .release
	yamllint -d "{extends: relaxed, rules: {line-length: {max: 350}}}" \
			collections/ansible_collections/*
	ANSIBLE_COLLECTIONS_PATHS=$(ANSIBLE_COLLECTIONS_PATHS) \
	ANSIBLE_COLLECTIONS_PATH=$(ANSIBLE_COLLECTIONS_PATHS) \
	ansible-lint collections/ansible_collections/*  > ansible-lint-results.txt; \
	cat ansible-lint-results.txt
	flake8 collections/ansible_collections/*

## TARGET: ansible-lint
## SYNOPSIS: make ansible-lint
## HOOKS: ansible-pre-lint, ansible-post-lint
## VARS: none
##
##  Perform lint checks on all Ansible collections and roles in the ./collections directory.

ansible-lint: ansible-pre-lint ansible-do-lint ansible-post-lint ## lint the Ansible collections

## TARGET: ansible-publish
## SYNOPSIS: make ansible-publish
## HOOKS: ansible-pre-publish, ansible-post-publish
## VARS: none
##
##  Publish all the collections in this repository.

ansible-pre-publish:

ansible-post-publish:

ansible-publish: ansible-pre-publish ansible-do-publish ansible-post-publish  ## publish the ansible collections to the repository

ansible-do-publish:
	$(ANSIBLE_SCRIPT_DIR)/ansible-publish.sh

# end of switch to suppress targets for help
endif
endif
