"""Description"""

__version__ = '1.0.0'

from core.service import Service
import logging


class Main(Service):
    """ Send incoming messages by email """
    def __init__(self, name='mailme', arguments=''):
        super().__init__(name)
        logging.debug('service \033[32m{}\033[0m loaded with arguments "\033[34m{}\033[0m"'.format(name, arguments))

    def on_schedule(self):
        while len(self._incoming_messages) > 0:
            (message, channel) = self._incoming_messages.pop()
            channel = self._bot.route(channel, 'email')
            self._outgoing_messages.insert(0, (message, channel))
            logging.debug('service \033[32mmailme\033[0m routed a message')
