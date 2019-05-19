PYTHON=python3
PIP=pip3

help:
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
	$(PYTHON) setup.py sdist
	$(PYTHON) setup.py bdist
	$(PYTHON) setup.py bdist_wheel

install:
	$(PIP) install --user dist/hypernet-0.1.tar.gz

run:
	$(PYTHON) hypernet.py

clean:
	rm -rf build
	rm -rf dist
	rm -rf hypernet.egg-info
	find -type f -name '*.pyc' -delete
	find -type d -name '__pycache__' -exec rmdir {} +

.PHONY: help build install run clean

