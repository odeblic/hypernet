from core.service import Service
import datetime
import logging


class Logme(Service):
    """ Log every incoming message """
    def __init__(self):
        super().__init__('logme', 1, None)

    def on_schedule(self):
        while len(self._incoming_messages) > 0:
            (message, channel) = self._incoming_messages.pop()
            with open('logme.txt', 'a') as f:
                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write('[{}]:\tmessage "{}" {}\n'.format(now, message, channel))
                logging.debug('service \033[32mlogme\033[0m logged a message')

