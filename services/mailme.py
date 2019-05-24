from core.service import Service
import logging


class Mailme(Service):
    """ Send incoming messages by email """
    def __init__(self):
        super().__init__('mailme', None, None)

    def on_schedule(self):
        while len(self._incoming_messages) > 0:
            (message, channel) = self._incoming_messages.pop()
            channel = self._bot.route(channel, 'email')
            self._outgoing_messages.insert(0, (message, channel))
            logging.debug('service \033[32mmailme\033[0m routed a message')
