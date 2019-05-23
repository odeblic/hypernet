import argparse
import logging
import time

from core.bot import Bot
from core.message import Message
from core.plugin import Plugin


def load_connectors():
    import connectors
    from core.connector import Connector
    return Plugin.discover(connectors, Connector)


class Framework(object):
    def __init__(self):
        self.__connectors = load_connectors()
        self.__bots = dict()
        self.__bots['innovate_bot_73'] = Bot('innovate_bot_73')

    def main(self):
        logging.info('The framework is starting')

        try:
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
                    logging.info('incoming message "{}" {}'.format(message, channel))
                    dispatched = False
                    for bot in self.__bots.values():
                        if bot.get_name() in message.find_elements(message.__class__.Mention) \
                            or channel.get_conversation() is None \
                            or bot.get_name() == channel.get_receiver():
                            dispatched = True
                            logging.debug('dispatched to bot \033[32m{}\033[0m'.format(bot.get_name()))
                            bot.deliver_incoming_message(message, channel)
                    if not dispatched:
                        logging.debug('no dispatching (no matching bot)')

                # trigger services for processing
                for bot in self.__bots.values():
                    bot.on_schedule()

                # collect outgoing messages
                outgoing_messages = list()
                for bot in self.__bots.values():
                    outgoing_messages += bot.fetch_outgoing_messages()

                # dispatch outgoing messages
                for (message, channel) in outgoing_messages:
                    logging.info('outgoing message "{}" {}'.format(message, channel))
                    dispatched = False
                    for connector in self.__connectors.values():
                        if channel.get_network() == connector.get_name():
                            dispatched = True
                            logging.debug('dispatched to network \033[32m{}\033[0m'.format(connector.get_name()))
                            connector.send_message(message, channel)
                    if not dispatched:
                        logging.debug('no dispatching (no matching network)')

        except KeyboardInterrupt:
            pass

        finally:
            for connector in self.__connectors.values():
                connector.stop()
            logging.info('The framework has stopped')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--log", default="/dev/stdout", help="output file for logs")
    arguments = parser.parse_args()

    logging.basicConfig(filename=arguments.log,
                        filemode='w',
                        level=logging.DEBUG,
                        format='[%(levelname)s]\t%(asctime)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    framework = Framework()
    framework.main()

