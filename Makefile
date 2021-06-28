.PHONY: help virtual-environment update-venv
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

virtual-environment: venv ## setup a virtual environment for development

venv: requirements.txt ## setup a virtual environment for development
	[ -d venv ] || python3 -m venv venv
	venv/bin/python -m pip install -r requirements.txt
	touch venv

update-venv:  ## update the development virtual environment
	[ -d venv ] || python3 -m venv venv
	venv/bin/python -m pip install --upgrade -r requirements.txt
	touch venv

download: venv download.py  ## download all the data
	venv/bin/python download.py
