from core.service import Service
import logging


class Echo(Service):
    """ Resend every incoming message to the sender """
    def __init__(self):
        super().__init__('echo', 1, None)

    def on_schedule(self):
        while len(self._incoming_messages) > 0:
            (message, channel) = self._incoming_messages.pop()
            channel = self._bot.reply(channel)
            message.set_first_mention(channel.get_receiver())
            self._outgoing_messages.insert(0, (message, channel))
            logging.debug('service \033[32mecho\033[0m replied a message')

