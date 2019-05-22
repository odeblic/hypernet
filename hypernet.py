import time


from core.connector import Connector
from core.message import Message
from core.plugin import Plugin
from core.service import Service

class Bot(object):
    def __init__(self, name):
        self.__name = name
        self.__connectors = dict()
        self.__services = dict()

    def main(self):
        print('The bot \033[32m{}\033[0m is starting.'.format(self.__name))
        try:
            self.__load_plugins()
            for connector in self.__connectors.values():
                connector.start()
            while True:
                time.sleep(1)

                # collect incoming messages
                incoming_messages = list()
                for connector in self.__connectors.values():
                    while True:
                        ret = connector.receive_message()
                        if ret is None: break
                        incoming_messages.append(ret)

                # dispatch incoming messages
                for (message, channel) in incoming_messages:
                    print('incoming message "{}" {}'.format(message, channel))
                    if self.__name in message.find_elements(message.__class__.Mention) or channel.get_conversation() is None:
                        for element in message.find_elements(message.__class__.Hashtag):
                            for name, service in self.__services.items():
                                if service.get_name() == element:
                                    print('dispatched to service \033[32m{}\033[0m'.format(service.get_name()))
                                    service.deliver_incoming_message(message, channel)

                # trigger services for processing
                for service in self.__services.values():
                    service.on_schedule()

                # collect outgoing messages
                outgoing_messages = list()
                for service in self.__services.values():
                    while True:
                        ret = service.fetch_outgoing_message()
                        if ret is None: break
                        outgoing_messages.append(ret)

                # dispatch outgoing messages
                for (message, channel) in outgoing_messages:
                    print('outgoing message "{}" {}'.format(message, channel))
                    for connector in self.__connectors.values():
                        connector.send_message(message, channel)

        except KeyboardInterrupt:
            pass
        finally:
            for connector in self.__connectors.values():
                connector.stop()
            print('The bot \033[32m{}\033[0m has stopped.'.format(self.__name))

    def __load_plugins(self):
        import connectors
        import services
        self.__connectors = Plugin.discover(connectors, Connector)
        self.__services = Plugin.discover(services, Service)


if __name__ == '__main__':
    bot = Bot('innovate_bot_73')
    bot.main()

