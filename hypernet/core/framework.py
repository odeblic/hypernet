import core.clock
import core.dispatcher
import core.hyperbot
import core.statistics
import core.user
import event.event
import logging
import time


from core.plugin import Plugin


class Framework(object):
    __instance = None

    def __init__(self, configuration):
        self.__loop_interval = configuration['core'].get('interval', 100) / 1000

        self.__clock = core.clock.Clock()
        self.__statistics = core.statistics.Statistics()

        self.__user_table = core.user.UserTable()

        self.__bots = dict()
        for user in configuration['core']['users']:
            name = user['framework_id']
            kind = user['kind']
            if kind == 'hyperbot':
                self.__bots[name] = core.hyperbot.NamedBot(name)
            else:
                roles = user.get('roles', [])
                new_user_event = event.event.make_user(name, kind, roles)
                self.__user_table.on_event(new_user_event)
        self.__default_bot = core.hyperbot.AnonymousBot()

        self.__dispatcher = core.dispatcher.Dispatcher(self.__bots)

        self.__service_list = list()
        for service in configuration['services']:
            name = service['plugin_id']
            self.__service_list.append(name)

        self.__network_list = list()
        for connector in configuration['connectors']:
            name = connector['plugin_id']
            self.__network_list.append(name)

        # send config events
        # receive ready events
        self.__running = False

    @classmethod
    def get_instance(cls, configuration=None):
        if cls.__instance is None:
            cls.__instance = cls(configuration)
        return cls.__instance
        # logging.error('The framework cannot have several instances')

    def main(self):
        self.__running = True
        logging.info('The framework is starting')
        try:
            while self.__running:
                start_time = time.monotonic()
                self.__dispatcher.on_schedule()
                self.__clock.on_schedule()
                stop_time = time.monotonic()
                duration = stop_time - start_time
                pause = self.__loop_interval - duration
                load_factor = 100 * (duration / self.__loop_interval)
                logging.debug('The load factor is {:.2f}%'.format(load_factor))
                if pause > 0:
                    time.sleep(pause)

        except KeyboardInterrupt:
            logging.info('Interruption from the user')
            self.__running = False

        finally:
            logging.info('The framework has stopped')

    def get_bot(self, name):
        bot = self.__bots.get(name, None)
        if bot is None:
            logging.warn('Invalid bot requested: {}'.format(name))
        return bot

    def get_default_bot(self):
        return self.__default_bot

    def get_clock(self):
        return self.__clock

    def get_statistics(self):
        return self.__statistics

    def get_user_table(self):
        return self.__user_table

    def get_network_list(self):
        return self.__network_list

    def get_service_list(self):
        return self.__service_list
