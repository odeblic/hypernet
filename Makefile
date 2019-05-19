help:
	@echo -e 'List of available targets:'
	@echo -e '\e[32m  help\e[0m    display help'
	@echo -e '\e[32m  build\e[0m   build the package'
	@echo -e '\e[32m  install\e[0m install the package'
	@echo -e '\e[32m  test\e[0m    run the program'
	@echo -e '\e[32m  clean\e[0m   cleanup the project'

build: deps
	pip3 install --user --upgrade setuptools wheel
	python setup.py sdist bdist_wheel

install:
	pip3 install dist/hypernet-*.whl

run:
	python hypernet.py

clean:
	rm -rf build
	rm -rf dist
	rm -rf hypernet.egg-info
	find -type f -name '*.pyc' -delete
	find -type d -name '__pycache__' -exec rmdir {} +

.PHONY: help init build install test clean

