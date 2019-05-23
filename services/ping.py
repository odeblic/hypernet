from core.service import Service
import logging


class Ping(Service):
    """ Ping test replying pong """
    def __init__(self):
        super().__init__('ping', None, None)

    def on_schedule(self):
        while len(self._incoming_messages) > 0:
            (message, channel) = self._incoming_messages.pop()
            channel = self.reply(channel)
            self._outgoing_messages.insert(0, (message.__class__.build('pong'), channel))
            logging.debug('service \033[32mping\033[0m reacted to a message')

    @staticmethod
    def reply(channel):
        sender = channel.get_receiver()
        receiver = channel.get_sender()
        conversation = channel.get_conversation()
        network = channel.get_network()
        return channel.__class__(sender, receiver, conversation, network)

