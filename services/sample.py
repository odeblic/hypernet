from core.service import Service
import logging


class Sample(Service):
    """ A sample to show how to implement a plugged-in service """
    def __init__(self):
        super().__init__('sample', 8, None)

    def on_schedule(self):
        while len(self._incoming_messages) > 0:
            (message, channel) = self._incoming_messages.pop()
            message = message.__class__.build('I am a #sample service and I do nothing')
            channel = self._bot.reply(channel)
            self._outgoing_messages.insert(0, (message, channel))
            logging.debug('service \033[32msample\033[0m replied to a message')

