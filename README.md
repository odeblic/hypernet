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

A **plugin** is a Python class declared as dynamically loadable by the bot to add features or implementation like services and connectors.

## Prerequisites

You need Python **3.6** or **3.7** with the following packages available:

- bidict
- nltk
- pyyaml

## Build

These tools are required to build the packages.

```pip3 install --upgrade setuptools wheel```

The following command generates the packages (tarball and wheel).

```python3 setup.py sdist bdist_wheel```

## Run

These dependencies are required to run the program.

```pip3 install -r requirements.txt```

Just run the main script without any argument.

```python3 hypernet.py```

## Installation

Just run one of these commands, depending on which packaging you opt for (tarball or wheel).

```pip3 install dist/hypernet-*.whl```
```pip3 install dist/hypernet-*.tar.gz```

## Makefile

For convenience, a set of target are available in a Makefile for common actions.

```make help```

## Author

Please contact me if you have any issue or question.

[Olivier de BLIC](mailto:odeblic@gmail.com)

## License

This program is under license MIT.
