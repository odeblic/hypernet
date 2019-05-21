from abc import abstractmethod
from core.plugin import Plugin
from core.translator import Translator
import threading
import time


class Connector(Plugin):
    def __init__(self, name, version, mtu, id_mapping):
        super().__init__(name, version)
        if mtu < 1:
            raise ValueError('Invalid mtu')
        self.__mtu = int(mtu)
        self.__thread = threading.Thread(target=self.__event_loop)
        self.__running = False
        self.__interval = float(0.1)
        self.__messages_to_network = list()
        self.__messages_from_network = list()
        self.__translator = Translator()
        for bot_id, net_id in id_mapping.items():
            self.__translator.add_agent(bot_id, net_id)

    def start(self):
        self.__running = True
        self.__thread.start()

    def stop(self):
        self.__running = False
        self.__thread.join()

    def get_mtu(self):
        return self.__mtu

    def send_message(self, message, channel):
        """ Enqueue outgoing messages (framework to network) """
        self.__messages_to_network.insert(0, (message, channel))

    def receive_message(self):
        """ Dequeue incoming messages (network to framework) """
        if len(self.__messages_from_network) > 0:
            return self.__messages_from_network.pop()
        else:
            return None

    def _pop_message_to_send(self):
        """ Dequeue outgoing messages (framework to network) """
        if len(self.__messages_to_network) > 0:
            (message, channel) = self.__messages_to_network.pop()
            channel = self.__translator.bot2net(channel)
            return (message, channel)
        else:
            return None

    def _push_received_message(self, message, channel):
        """ Enqueue incoming messages (network to framework) """
        channel = self.__translator.net2bot(channel)
        self.__messages_from_network.insert(0, (message, channel))

    @abstractmethod
    def _on_schedule(self):
        """ this method will be called repeatedly from an event loop """
        pass

    def __event_loop(self):
        while self.__running:
            time.sleep(self.__interval)
            self._on_schedule()

