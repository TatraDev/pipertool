SHELL:=/usr/bin/env bash

.PHONY: lint
lint:
	flake8 piper

.PHONY: unit
unit:
	pytest tests/running_piper_test.py::TestVenv

.PHONY: package
package:
	pip check

.PHONY: test
test: package unit
