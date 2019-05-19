from abc import abstractmethod
from core.plugin import Plugin


class Service(Plugin):
    def __init__(self, name, version, configuration):
        super().__init__(name, version)
        self.__configuration = configuration

    def get_configuration(self):
        return self.__configuration

    @abstractmethod
    def on_message(self, message):
        pass

    def send_message(self, message):
        pass

