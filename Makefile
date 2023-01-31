SHELL:=/usr/bin/env bash

.PHONY: lint unit package test jupyter

lint:
	flake8 piper

unit:
	# pytest -vs tests/import_test.py
	# pytest -vs tests/base_executor_test.py
	# pytest -vs tests/base_test.py
	# pytest -vs tests/envs_test.py::TestCompose
	# pytest -vs tests/envs_test.py::TestVenv
	pytest -vs tests/clip_test.py

package:
	pip check

test: package unit

jupyter:
	docker run -it --rm -p 10000:8888 -v "${PWD}":/home/jovyan/work jupyter/datascience-notebook:b418b67c225b

clean_applications:
	rm -rf applications
	mkdir applications