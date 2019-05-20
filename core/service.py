from abc import abstractmethod
from core.plugin import Plugin


class Service(Plugin):
    def __init__(self, name, version, configuration):
        super().__init__(name, version)
        self.__configuration = configuration
        self._incoming_messages = list()
        self._outgoing_messages = list()

    def get_configuration(self):
        return self.__configuration

    def deliver_incoming_message(self, message, channel):
        self._incoming_messages.insert(0, (message, channel))

    def fetch_outgoing_message(self):
        if len(self._outgoing_messages) > 0:
            return self._outgoing_messages.pop()
        else:
            return None

    @abstractmethod
    def on_schedule(self):
        pass

