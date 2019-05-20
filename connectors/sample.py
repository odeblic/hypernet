from core.channel import Channel
from core.connector import Connector


class Sample(Connector):
    """ A sample to show how to implement a plugged-in connector """
    def __init__(self):
        super().__init__('sample', 7, 512, {'bot_id':111, 'net_id':999})

    def _on_schedule(self):
        # example of incoming message
        sender = 111
        receiver = 999
        conversation = None
        channel = Channel(sender, receiver, conversation)
        print('incoming message "{}" from {} to {} within {}'.format(message, sender, receiver, conversation))
        self._push_received_message('Hello world', channel)

        # example of outgoing message
        (message, channel) = self._pop_message_to_send()
        (sender, receiver, conversation) = channel
        print('outgoing message "{}" from {} to {} within {}'.format(message, sender, receiver, conversation))

