#!/usr/bin/env python3

import argparse
import core.framework
import logging
import sys
import yamale
import yaml


def load_configuration(filename):
    try:
        schema = yamale.make_schema('hypernet/data/model.yaml')
        data = yamale.make_data(filename)
        # yamale.validate(schema, data)
    except ValueError as e:
        logging.error('error during validation: {}'.format(e))
        return None
    try:
        with open(filename, 'r') as f:
            configuration = yaml.safe_load(f)
    except yaml.YAMLError as e:
        logging.error('could not read the YAML file: {}'.format(e))
        return None
    return configuration


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", default=None, help="output file for logs")
    parser.add_argument("cfg", help="configuration file")
    arguments = parser.parse_args()

    configuration = load_configuration(arguments.cfg)

    logging.basicConfig(filename=arguments.log,
                        filemode='w',
                        level=logging.INFO,
                        format='[%(levelname)s]\t%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    try:
        instance = core.framework.Framework.get_instance(configuration)
        instance.main()
    except Exception as e:
        logging.critical('The framework has aborted because of exception: {}'.format(e))
        # logging.exception('The framework has aborted because of exception: {}'.format(e))
        raise


if __name__ == '__main__':
    sys.exit(main())
