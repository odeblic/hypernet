from core.connector import Connector


class Sample(Connector):
    """ A sample to show how to implement a plugged-in connector """
    def __init__(self):
        super().__init__('sample', 1, 512, {'bot_id':'111', 'net_id':'999'})

    def post(self, message, receiver, conversation):
        print('post message "{}" to {}@{}'.format(message, receiver, conversation))

    def on_schedule(self):
        pass

