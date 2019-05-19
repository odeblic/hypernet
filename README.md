# Hypernet

## Introduction

This framework is aimed to provide services among users and bots, over interconnected networks.

Different users and bots can communicate cross networks seamlessly.

In short, this is communication:

- whoever
- whatever
- wherever

## Description

The project consists of a main program that runs as a daemon and loads services and connectors as plugins.

A **service** is a subbot able to send and receive messages related to the feature implementated.

A **connector** handles the connection to a network, with a dedicated account. It abstracts the format of messages to match the internal representation used within the framework.

## Prerequisites

You need Python **3.6** or **3.7** with the following packages available:

- bidict
- nltk
- pyyaml

## Build

These tools are required to build the package.

```python -m pip install --user --upgrade setuptools wheel```

The following command generate the packages (tarball and wheel).

```python setup.py sdist bdist_wheel```

## Installation

Just run one of these commands, depending on which packaging you opt for (tarball or wheel).

```pip install dist/hypernet-*.whl```
```pip install dist/hypernet-*.tar.gz```

## Makefile

For convenience, a set of target are available in a Makefile for common actions.

```make help```

## Author

Please contact me if you have any issue or question.

[Olivier de BLIC](mailto:odeblic@gmail.com)

## License

This program is under license MIT.
