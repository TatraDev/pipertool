SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	flake8 piper

.PHONY: unit
unit:
	pytest -vs tests/running_piper_test.py::TestCompose

.PHONY: package
package:
	pip check

.PHONY: test
test: package unit

jupyter:
	docker run -it --rm -p 10000:8888 -v "${PWD}":/home/jovyan/work jupyter/datascience-notebook:b418b67c225b