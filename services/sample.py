from core.service import Service


class Sample(Service):
    """ A sample to show how to implement a plugged-in service """
    def __init__(self):
        super().__init__('sample', 8, None)

    def _on_schedule(self):
        pass

    def on_message(self, message, channel):
        sender = channel.get_sender()
        receiver = channel.get_receiver()
        conversation = channel.get_conversation()
        print('incoming message "{}" from {} to {} within {}'.format(message, sender, receiver, conversation))

