from core.message import Message
from core.service import Service
import datetime
import logging


class Alarm(Service):
    """ Send back a message after a period of time """
    def __init__(self):
        super().__init__('alarm', 1, None)
        self.__alarms = list()

    def on_schedule(self):
        now = datetime.datetime.now()

        while len(self._incoming_messages) > 0:
            (message, channel) = self._incoming_messages.pop()
            logging.debug('alarm:\tincoming message "{}" {}'.format(message, channel))
            seconds = self.extract_time(message)
            if seconds is not None:
                self.__alarms.append((now, seconds, channel))
            else:
                channel = self.reply(channel)
                message = Message.build('#alarm service does not understand your request')
                self._outgoing_messages.insert(0, (message, channel))

        triggered = list()
        waiting = list()

        for (timestamp, seconds, channel) in self.__alarms:
            alarm_time = timestamp + datetime.timedelta(seconds=seconds)
            if alarm_time > now:
                waiting.append((timestamp, seconds, channel))
            else:
                triggered.append((timestamp, seconds, channel))

        for (timestamp, seconds, channel) in triggered:
            message = Message.build('#alarm service has been requested {} seconds ago'.format(seconds))
            channel = self.reply(channel)
            self._outgoing_messages.insert(0, (message, channel))
            logging.debug('alarm:\toutgoing message "{}" {}'.format(message, channel))

        self.__alarms = waiting

    @staticmethod
    def extract_time(message):
        numbers = message.find_elements(message.__class__.Number)
        if len(numbers) > 0 and numbers[0] > 0:
            return numbers[0]
        else:
            return None

    @staticmethod
    def reply(channel):
        sender = channel.get_receiver()
        receiver = channel.get_sender()
        conversation = channel.get_conversation()
        network = channel.get_network()
        return channel.__class__(sender, receiver, conversation, network)

