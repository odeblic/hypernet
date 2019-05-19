from abc import ABC, abstractmethod
from core.plugin import Plugin


class Service(Plugin):
    def __init__(self, name, version, configuration):
        self.__name = str(name)
        self.__version = int(version)
        self.__configuration = object(configuration)

    def get_name(self):
        return self.__name

    def get_version(self):
        return self.__version

    def get_configuration(self):
        return self.__configuration

    @abstractmethod
    def on_message(self, message):
        pass

    def send_message(self, message):
        pass

