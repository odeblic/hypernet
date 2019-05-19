import connectors
import services
import time


from core.plugin import Plugin
from core.service import Service
from core.connector import Connector


class Bot(object):
    def __init__(self, name, connectors, services):
        self.__name = str(name)
        self.__connectors = list(connectors)
        self.__services = list(services)

    def main(self):
        print('The bot \033[32m{}\033[0m is starting.'.format(self.__name))
        try:
            while True:
                print('Hello world! I\'m \033[32m{}\033[0m!'.format(self.__name))
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        finally:
            print('The bot \033[32m{}\033[0m has stopped.'.format(self.__name))


if __name__ == '__main__':
    connectors = Plugin.discover(connectors, Connector)
    services = Plugin.discover(services, Service)
    bot = Bot('globot', connectors, services)
    bot.main()

