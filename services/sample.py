from core.service import Service


class Sample(Service):
    """ A sample to show how to implement a plugged-in service """
    def __init__(self):
        super().__init__('sample', 8, None)

    def on_schedule(self):
        while len(self._incoming_messages) > 0:
            (message, channel) = self._incoming_messages.pop()
            print('service:\tincoming message "{}" {}'.format(message, channel))

            message = message.__class__.build('Here is #sample service. What can I do for you?')
            sender = channel.get_receiver()
            receiver = channel.get_sender()
            conversation = channel.get_conversation()
            channel = channel.__class__(sender, receiver, conversation)
            self._outgoing_messages.insert(0, (message, channel))
            print('service:\toutgoing message "{}" {}'.format(message, channel))

