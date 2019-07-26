"""Description"""

__version__ = '1.0.0'

from core.channel import Channel
from core.service import Service
from core.message import Message
import datetime
import logging


class Main(Service):
    """ Measure the latency to remote bots and print a report on demand """
    INTERVAL = datetime.timedelta(seconds=5)

    def __init__(self, name='discovery', arguments=''):
        super().__init__(name)
        logging.debug('service \033[32m{}\033[0m loaded with arguments "\033[34m{}\033[0m"'.format(name, arguments))
        self.__bots = dict({'bot89':None, 'bot73':None})
        self.__pending = dict()
        self.__active = False

    def on_schedule(self):
        while len(self._incoming_messages) > 0:
            (message, channel) = self._incoming_messages.pop()
            now = datetime.datetime.now()

            if 'activate' in message.find_elements(message.__class__.Word):
                logging.debug('service \033[32mdiscovery\033[0m has been activated')
                self.__active = True
            elif 'deactivate' in message.find_elements(message.__class__.Word):
                logging.debug('service \033[32mdiscovery\033[0m has been deactivated')
                self.__active = False
            elif 'trigger' in message.find_elements(message.__class__.Word):
                logging.debug('service \033[32mdiscovery\033[0m has been triggered')
                for bot_name in self.__bots.keys():
                    if bot_name != self._bot.get_name():
                        self.__pending[bot_name] = now
                        message = Message.build('@{} #discovery token 1'.format(bot_name))
                        channel = Channel(self._bot.get_name(), bot_name, channel.get_conversation(), channel.get_network())
                        self._outgoing_messages.insert(0, (message, channel))
                        logging.debug('service \033[32mdiscovery\033[0m has sent a token')
            elif 'report' in message.find_elements(message.__class__.Word):
                logging.debug('service \033[32mdiscovery\033[0m made a report')
                bots = list()
                for (name, latency) in self.__bots.items():
                    bots.append('{} {}'.format(name, latency))
                message = Message.build(' '.join(bots))
                channel = self._bot.reply(channel)
                message.set_first_mention(channel.get_receiver())
                self._outgoing_messages.insert(0, (message, channel))
            elif 'token' in message.find_elements(message.__class__.Word):
                bot_name = channel.get_sender()
                if bot_name in self.__pending.keys():
                    latency = now - self.__pending[bot_name]
                    latency = latency.seconds + latency.microseconds / 1000000
                    logging.debug('service \033[32mdiscovery\033[0m has received a token (latency: {} seconds)'.format(latency))
                    self.__bots[bot_name] = int(latency)
                if self.__active:
                    self.__pending[bot_name] = now
                    channel = self._bot.reply(channel)
                    message.set_first_mention(channel.get_receiver())
                    message.increment_numbers()
                    self._outgoing_messages.insert(0, (message, channel))
                    logging.debug('service \033[32mdiscovery\033[0m has sent a token')
                else:
                    del(self.__pending[bot_name])

