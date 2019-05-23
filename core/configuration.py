#import json
import yaml


class Configuration(object):
    def __init__(self, path):
        with open(path, 'r') as f:
            #self.__content = json.load(f)
            self.__content = yaml.safe_load(f)

    def get(self):
        return self.__content

# permissions

