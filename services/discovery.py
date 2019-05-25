from core.channel import Channel
from core.service import Service
from core.message import Message
import datetime
import logging


class Discovery(Service):
    """ Measure the latency to remote bots and print a report on demand """
    INTERVAL = datetime.timedelta(seconds=5)

    def __init__(self):
        super().__init__('discovery', 1, None)
        self.__bots = dict({'bot89':None, 'bot73':None})
        self.__pending = dict()
        self.__before = datetime.datetime.now()
        self.__active = False

    def on_schedule(self):
        # use a pattern req/resp or daemon?
        while len(self._incoming_messages) > 0:
            (message, channel) = self._incoming_messages.pop()
            now = datetime.datetime.now()

            if 'start' in message.find_elements(message.__class__.Word):
                logging.debug('service \033[32mdiscovery\033[0m has been activated')
                self.__active = True
                for name in self.__bots.keys():
                    if name != self._bot.get_name():
                        self.__pending[name] = now
                        message = Message.build('@{} #discovery seqnum 1'.format(name))
                        channel = Channel(self._bot.get_name(), name, channel.get_conversation(), channel.get_network())
                        self._outgoing_messages.insert(0, (message, channel))
                        logging.debug('service \033[32mdiscovery\033[0m sent a request')
                self.__before = now
            elif 'stop' in message.find_elements(message.__class__.Word):
                logging.debug('service \033[32mdiscovery\033[0m has been deactivated')
                self.__active = False
            elif 'status' in message.find_elements(message.__class__.Word):
                logging.debug('service \033[32mdiscovery\033[0m reported its status')
                bots = list()
                for (name, latency) in self.__bots.items():
                    bots.append('{} {}'.format(name, latency))
                message = Message.build(' '.join(bots))
                channel = self._bot.reply(channel)
                message.set_first_mention(channel.get_receiver())
                self._outgoing_messages.insert(0, (message, channel))
            elif 'seqnum' in message.find_elements(message.__class__.Word) and self.__active:
                logging.debug('service \033[32mdiscovery\033[0m has been triggered')
                #bot_name = channel.get_sender()
                #if channel.get_sender() in self.__pending.keys():
                #if channel.get_sender() in self.__bots.keys():
                #logging.debug('service \033[32mdiscovery\033[0m received a response')
                #request_time = self.__pending[bot_name]
                #response_time = datetime.datetime.now()
                #latency = response_time - request_time
                #self.__bots[bot_name] = latency.seconds

                #channel = self._bot.forward(channel, 'bot89')
                #message = Message.build('@bot89 #discovery seqnum 47')
                channel = self._bot.reply(channel)
                message.set_first_mention(channel.get_receiver())
                message.increment_numbers()
                self._outgoing_messages.insert(0, (message, channel))
                #else:
                #    logging.error('service \033[32mdiscovery\033[0m received a response by mistake')

        return

            # respond to requests if any

        # periodically ping other bots
        #if self.__active:
        #self.__active = False
        now = datetime.datetime.now()
        if now - self.__before > self.INTERVAL:
            for name in self.__bots.keys():
                self.__pending[name] = now
                message = Message.build('@bot89 #discovery 1')
                channel = Channel('bot73', 'bot89', 'cool', 'symphony')
                self._outgoing_messages.insert(0, (message, channel))
                logging.debug('service \033[32mdiscovery\033[0m sent a request')
            self.__before = now

