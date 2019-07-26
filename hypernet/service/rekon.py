"""Description"""

__version__ = '1.0.0'

from core.service import Service
import logging


class Main(Service):
    """ Reconciliation of missing trades """
    def __init__(self, name='rekon', arguments=''):
        super().__init__(name)
        logging.debug('service \033[32m{}\033[0m loaded with arguments "\033[34m{}\033[0m"'.format(name, arguments))

    def on_schedule(self):
        if len(self._incoming_messages) > 0:
            self._incoming_messages = list()

