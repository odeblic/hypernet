"""Description"""

__version__ = '1.0.0'

from core.channel import Channel
from core.service import Service
from core.message import Message
import datetime
import logging


class Main(Service):
    """ Send periodically a chirp to other bots """
    INTERVAL = datetime.timedelta(seconds=45)

    def __init__(self, name='beacon', arguments=''):
        super().__init__(name)
        logging.debug('service \033[32m{}\033[0m loaded with arguments "\033[34m{}\033[0m"'.format(name, arguments))
        self.__bots = dict({'bot89':None, 'bot73':None})
        self.__before = datetime.datetime.now()

    def on_schedule(self):
        now = datetime.datetime.now()
        if now - self.__before > self.INTERVAL:
            for bot_name in self.__bots.keys():
                if bot_name != self._bot.get_name():
                    #self.__pending[bot_name] = now
                    message = Message.build('@{} chirp'.format(bot_name))
                    channel = Channel(self._bot.get_name(), bot_name, 'cool', 'symphony')
                    self._outgoing_messages.insert(0, (message, channel))
                    logging.debug('service \033[32mbeacon\033[0m sent a chirp')
            self.__before = now

