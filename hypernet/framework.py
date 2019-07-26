import logging
import time
import yamale
import yaml


__all__ = ['', '', '']


from core.plugin import Plugin
#from core.bot import Bot


class Configuration(object):
    def __init__(self, path):
        with open(path, 'r') as f:
            self.__content = yaml.safe_load(f)

    def get(self):
        return self.__content


class Framework(object):
    def __init__(self, config_filename):
        validate_configuration(config_filename, 'schema.yaml')
        load_configuration(config_filename)
        # start dispatcher
        # start clock
        # start user table
        # start connectors
        # start services
        # send config events
        # receive ready events

    @staticmethod
    def validate_configuration(config_filename, schema_filename):
        try:
            schema = yamale.make_schema(schema_filename)
            data = yamale.make_data(config_filename)
            yamale.validate(schema, data)
        except yaml.YAMLError as e:
            logging.error('error during validation: {}'.format(e))
            raise

    def load_configuration(self, config_filename):
        try:
            with open(config_file, 'r') as f:
                self.__configuration = yaml.safe_load(f)
        except yaml.YAMLError as e:
            logging.error('could not read the YAML file: {}'.format(e))
            raise

    def main(self):
        logging.info('The framework is starting')
        loop_interval = 0.1
        while True:
            start_time = time.monotonic()
            dispatcher.on_schedule()
            clock.on_schedule()
            stop_time = time.monotonic()
            duration = stop_time - start_time
            pause = loop_interval - duration
            load_factor = 100 * (duration / loop_interval)
            if pause > 0:
                time.sleep(pause)

        try:


        except KeyboardInterrupt:
            pass

        finally:
            logging.info('The framework has stopped')
