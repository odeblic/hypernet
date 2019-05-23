from core.channel import Channel
from core.service import Service
from core.message import Message
import datetime
import logging


class Discovery(Service):
    """ Measure the latency to remote bots and print a report on demand """
    INTERVAL = datetime.timedelta(seconds=3)

    def __init__(self):
        super().__init__('discovery', 1, None)
        self.__bots = dict({'innovate_bot_89':1000000})
        self.__pending = dict()
        self.__before = datetime.datetime.now()

    def on_schedule(self):
        return
        while len(self._incoming_messages) > 0:
            (message, channel) = self._incoming_messages.pop()

            # measure latency for responses if any
            bot_name = channel.get_sender()
            if channel.get_sender() in self.__pending:
                logging.debug('service \033[32mdiscovery\033[0m received a response')
                request_time = self.__pending[bot_name]
                response_time = datetime.datetime.now()
                latency = response_time - request_time
                self.__bots[bot_name] = latency.seconds
            else:
                logging.error('service \033[32mdiscovery\033[0m received a response by mistake')

            # respond to requests if any
            bots = list()
            for (name, latency) in self.__bots.items():
                bots.append('{} {}'.format(name, latency))
            message = Message.build(' '.join(bots))
            channel = self._bot.reply(channel)
            self._outgoing_messages.insert(0, (message, channel))
            logging.debug('service \033[32mdiscovery\033[0m has been requested')

        # periodically ping other bots
        now = datetime.datetime.now()
        if now - self.__before > self.INTERVAL:
            for name in self.__bots.keys():
                self.__pending[name] = now
                message = Message.build('@innovate_bot_89 #echo #discovery')
                channel = Channel('innovate_bot_73', 'innovate_bot_89', 'cool', 'symphony')
                self._outgoing_messages.insert(0, (message, channel))
                logging.debug('service \033[32mdiscovery\033[0m is searching...')
            self.__before = now

