from core.channel import Channel
from core.connector import Connector
from core.message import Message
import time


class Sample(Connector):
    """ A sample to show how to implement a plugged-in connector """
    def __init__(self):
        super().__init__('sample', 7, 512, {'Globot':0, 'Jack Eleven':11, 'Anna Five':5})

    def _on_schedule(self):
        """ This method is called repeatedly from an event loop """

        # sender/receiver/stream id's are automatically translated by the base class Connector
        # when calling methods _pop_message_to_send() and _push_received_message()

        # example of incoming message for the bot in private
        message = Message.build('Hi @globot please ask for service #sample')
        channel = Channel(11, 0, None)
        print('connector:\tincoming message "{}" {}'.format(message, channel))
        self._push_received_message(message, channel)

        # example of incoming message for the bot in chatroom
        message = Message.build('Hi @globot please ask for service #sample')
        channel = Channel(60, 0, 777)
        print('connector:\tincoming message "{}" {}'.format(message, channel))
        self._push_received_message(message, channel)

        # example of incoming message in chatroom for another agent
        message = Message.build('Hi there, nothing new today...')
        channel = Channel(11, 60, 777)
        print('connector:\tincoming message "{}" {}'.format(message, channel))
        self._push_received_message(message, channel)

        # example of outgoing message
        while True:
            ret = self._pop_message_to_send()
            if ret is None: break
            (message, channel) = ret
            print('connector:\toutgoing message "{}" {}'.format(message, channel))

