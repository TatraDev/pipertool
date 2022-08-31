SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	flake8 piper

.PHONY: unit
unit:
	pytest -vs tests/running_piper_test.py::TestDifferentEnv

.PHONY: package
package:
	pip check

.PHONY: test
test: package unit
