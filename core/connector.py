from abc import abstractmethod
from core.plugin import Plugin
from core.translator import Translator
import threading


class Connector(Plugin):
    def __init__(self, name, version, mtu, id_mapping):
        super().__init__(name, version)
        if mtu < 1:
            raise ValueError('Invalid mtu')
        self.__mtu = int(mtu)
        self.__thread = threading.Thread(target=self.event_loop)
        self.__callback = None
        self.__running = False
        self.agents = Translator(id_mapping)
        self.conversations = Translator()

    def get_mtu(self):
        return self.__mtu

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
            sender = self.agents.net2bot(sender)
            receiver = self.agents.net2bot(receiver)
            conversation = self.conversations.net2bot(conversation)
            channel = Channel(sender, receiver, conversation)
            self.__callback(message, channel)

    def send_message(self, message, channel):
        sender = self.agents.bot2net(channel.get_sender())
        receiver = self.agents.bot2net(channel.get_receiver())
        conversation = self.conversations.bot2net(channel.get_conversation())
        self.post(message, sender, receiver, conversation)

    @abstractmethod
    def on_schedule(self):
        pass

    @abstractmethod
    def post(self, message, sender, receiver, conversation):
        pass

