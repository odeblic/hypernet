from abc import ABC, abstractmethod
import bidict
from core.plugin import Plugin
import re
import threading


class Connector(ABC, Plugin):
    def __init__(self, name, mtu, id_mapping):
        super().__init__()
        pattern = re.compile("^[a-z][a-z0-9]+$")
        if not pattern.match(name):
            raise ValueError('Invalid name for Network')
        self.__name = str(name)
        if mtu < 1:
            raise ValueError('Invalid mtu')
        if len(id_mapping) < 1:
            raise ValueError('At least one user must be defined')
        self.__mtu = int(mtu)
        self.__id_mapping = bidict.bidict(id_mapping)
        self.__thread = threading.Thread(target=self.event_loop)
        self.__callback = None
        self.__running = False

    def get_name(self):
        return self.__name

    def get_mtu(self):
        return self.__mtu

    def translate_id_bot2net(self, identifier):
        return self.__id_mapping[identifier]

    def translate_id_net2bot(self, identifier):
        return self.__id_mapping.inverse[identifier]

    def event_loop(self):
        while self.__running:
            self.on_schedule()

    def subscribe(self, callback):
        self.__callback = callback

    def start(self):
        self.__running = True
        self.__thread.start()

    def stop(self):
        self.__running = False
        self.__thread.join()

    def on_receive_message(self, message, sender, conversation):
        if self.__callback is not None:
            sender = self.translate_id_net2bot(sender)
            self.__callback(message, sender, conversation)

    def send_message(self, message, receiver, conversation):
        receiver = self.translate_id_bot2net(receiver)
        self.post(message, receiver, conversation)

    @abstractmethod
    def on_schedule(self):
        pass

    @abstractmethod
    def post(self, message, receiver, conversation):
        pass

