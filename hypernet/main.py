#!/usr/bin/env python3

import argparse
import framework
import logging
import sys


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", default=None, help="output file for logs")
    parser.add_argument("cfg", required=True, help="configuration file")
    arguments = parser.parse_args()

    logging.basicConfig(filename=arguments.log,
                        filemode='w',
                        level=logging.INFO,
                        format='[%(levelname)s]\t%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    try:
        framework.Framework(arguments.cfg).main()
    except Exception as e:
        logging.critical('The framework has aborted because of exception: {}'.format(e))
        logging.exception('The framework has aborted because of exception: {}'.format(e))
        raise


if __name__ == '__main__':
    sys.exit(main())

