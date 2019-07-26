"""Generic class to be extended to implement a connector"""

import abc
from core.plugin import Plugin
from core.translator import Translator
import logging
import threading
import time


# ascii, utf8, binary

class Connector(Plugin):
    def __init__(self, arguments, endpoint):
        super().__init__()
        agents = configuration['networks'][name]['agents']

        for agent in agents.values():
            bot_id = agent['local_id']
            net_id = agent['global_id']
            kind = agent['kind']
            self.__translator.add_agent(bot_id, net_id)

        self.__thread = threading.Thread(target=self.__event_loop)
        self.__running = False
        self.__interval = float(0.1)

    def start(self):
        self.__running = True
        self.__thread.start()

    def stop(self):
        self.__running = False

    def is_running(self):
        return self.__running

    def wait(self):
        self.__thread.join()

    def __event_loop(self):
        """Main event loop"""
        try:
            while self.__running:
                time.sleep(self.__interval)
                self._on_schedule()
        except KeyboardInterrupt:
            logging.info('interruption from user')
        except Exception as e:
            logging.exception('exception!!!')
        finally:
            self.__running = False

    @abs.abstractmethod
    def __on_schedule(self):
        """This method will be called repeatedly from the event loop"""
        pass

    def get_mtu(self):
        """ Get the maximum size of the payload for a message (in bytes) """
        return self.__mtu

