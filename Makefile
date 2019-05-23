PYTHON := $(shell which python3.7 || which python3.6)
PIP := $(shell which pip3)
VERSION := $(shell git describe --tags --dirty)

help:
	@printf 'Welcome to the project \e[33mHypernet\e[0m\n'
	@printf '(version \e[35m'$(VERSION)'\e[0m)\n\n'
	@echo -e 'List of available targets:'
	@printf '\e[32m   help\e[0m     display help\n'
	@printf '\e[32m   deps\e[0m     install dependencies\n'
	@printf '\e[32m   build\e[0m    build the package\n'
	@printf '\e[32m   install\e[0m  install the package\n'
	@printf '\e[32m   run\e[0m      run the program\n'
	@printf '\e[32m   clean\e[0m    cleanup the project\n'

deps:
	$(PIP) install --user --upgrade setuptools wheel
	$(PIP) install --user -r requirements.txt

build:
	echo -n $(VERSION) > version.txt
	$(PYTHON) setup.py bdist

install:
	$(PIP) install --user dist/hypernet-$(VERSION).*.tar.gz

run:
	$(PYTHON) hypernet.py

clean:
	rm -rf build
	rm -rf dist
	rm -rf hypernet.egg-info
	rm -rf version.txt
	find -type f -name '*.pyc' -delete
	find -type d -name '__pycache__' -exec rmdir {} +

.PHONY: help deps build install run clean

