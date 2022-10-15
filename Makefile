SHELL:=/usr/bin/env bash

.PHONY: lint unit package test jupyter

lint:
	flake8 piper

unit:
	pytest -vs tests/envs_test.py::TestCompose

package:
	pip check

test: package unit

jupyter:
	docker run -it --rm -p 10000:8888 -v "${PWD}":/home/jovyan/work jupyter/datascience-notebook:b418b67c225b