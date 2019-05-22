from core.service import Service
import logging


class Blackhole(Service):
    """ Swallow every incoming message """
    def __init__(self):
        super().__init__('blackhole', 1, None)

    def on_schedule(self):
        if len(self._incoming_messages) > 0:
            logging.debug('service \033[32mblackhole\033[0m swallowed {} message(s)'.format(len(self._incoming_messages)))
            self._incoming_messages = list()

