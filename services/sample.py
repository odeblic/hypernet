from core.service import Service


class Sample(Service):
    """ A sample to show how to implement a plugged-in service """
    def __init__(self):
        super().__init__('sample', 1, None)

    def on_message(self, message, channel):
        sender = channel.get_sender()
        conversation = channel.get_conversation()
        print('got message "{}" from {}@{}'.format(message, sender, conversation))

