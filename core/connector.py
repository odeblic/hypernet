from abc import abstractmethod
import bidict
from core.plugin import Plugin
import threading


class Connector(Plugin):
    def __init__(self, name, version, mtu, id_mapping):
        super().__init__(name, version)
        if mtu < 1:
            raise ValueError('Invalid mtu')
        if len(id_mapping) < 1:
            raise ValueError('At least one user must be defined')
        self.__mtu = int(mtu)
        self.__id_mapping = bidict.bidict(id_mapping)
        self.__thread = threading.Thread(target=self.event_loop)
        self.__callback = None
        self.__running = False

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

    def on_receive_message(self, message, sender, receiver, conversation):
        if self.__callback is not None:
            sender = self.translate_id_net2bot(sender)
            receiver = self.translate_id_net2bot(receiver)
            channel = Channel(sender, receiver, conversation)
            self.__callback(message, channel)

    def send_message(self, message, channel):
        sender = self.translate_id_bot2net(channel.get_sender())
        receiver = self.translate_id_bot2net(channel.get_receiver())
        conversation = channel.get_conversation()
        self.post(message, sender, receiver, conversation)

    @abstractmethod
    def on_schedule(self):
        pass

    @abstractmethod
    def post(self, message, sender, receiver, conversation):
        pass

