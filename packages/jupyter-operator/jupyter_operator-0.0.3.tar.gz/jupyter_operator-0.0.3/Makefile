# Copyright (c) Datalayer, Inc. https://datalayer.io
# Distributed under the terms of the MIT License.

SHELL=/bin/bash

CONDA=source $$(conda info --base)/etc/profile.d/conda.sh
CONDA_ACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda activate
CONDA_DEACTIVATE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda deactivate
CONDA_REMOVE=source $$(conda info --base)/etc/profile.d/conda.sh ; conda remove -y --all -n

ENV_NAME=jupyter-operator

.DEFAULT_GOAL := default

.SILENT: init

.PHONY: port-forward storybook

help: ## display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m<target>\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

default: help ## default target is help

env: warning ## env
	($(CONDA); \
		SLUGIFY_USES_TEXT_UNIDECODE=yes conda env create -n jupyter-operator -f ${DATALAYER_HOME}/src/environment.yml )
	@exec echo "You can now populate the jupyter-operator environment."
	@exec echo "-------------------------------------------------------"
	@exec echo "conda activate ${ENV_NAME}"
	@exec echo "-------------------------------------------------------"


env-rm: warning ## env-rm
	($(CONDA); \
		conda deactivate && \
		conda remove -y --name ${ENV_NAME} --all || true )

env-status: ## env-status
	($(CONDA_ACTIVATE) ${ENV_NAME}; \
		./../bin/dla env-status )

kill:
	./dev/utils/kill.sh

warning:
	echo "\x1b[34m\x1b[43mEnsure you have run \x1b[1;37m\x1b[41m conda deactivate \x1b[22m\x1b[34m\x1b[43m before invoking this.\x1b[0m"

publish: clean build ## publish
	($(CONDA_ACTIVATE) ${ENV_NAME}; \
		npm publish )
	echo open https://www.npmjs.com/package/@datalayer/jupyter-operator

typedoc: ## generate typedoc
	($(CONDA_ACTIVATE) ${ENV_NAME}; \
		rm -fr typedoc && \
		yarn typedoc --tsconfig ./tsconfig.json && \
		open typedoc/index.html )

publish-typedoc: typedoc ## deploy typedoc
	aws s3 rm \
		s3://datalayer-typedoc/datalayer/jupyter-operator/0.0.3/ \
		--recursive \
		--profile datalayer
	aws s3 cp \
		typedoc \
		s3://datalayer-typedoc/datalayer/jupyter-operator/0.0.3/ \
		--recursive \
		--profile datalayer
	aws cloudfront create-invalidation \
		--distribution-id E1CPG9FNSQJESH \
		--paths /datalayer/jupyter-operator/0.0.3/ \
		--profile datalayer
	echo open ✨  https://typedoc.datalayer.tech/datalayer/jupyter-operator/0.0.3
