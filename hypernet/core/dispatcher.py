import core.framework
import logging
import queue


class Dispatcher(object):
    """ Manager responsible for events delivery from/to the right connector/bot """
    class Endpoint(object):
        """ Handler embedding the logic to send/receive events within the connector """
        def __init__(self, network, incoming_queue, outgoing_queue, mapping):
            self.__network = network
            self.__incoming_queue = incoming_queue
            self.__outgoing_queue = outgoing_queue
            self.__translator = translator(mapping)
            # service for message dump and recovery

        # message
        # sender, receiver, conversation
        # (network set automatically)
        # blocking=False
        def push(self, msg):
            """ Enqueue incoming events (network to framework) """
            self.__translator.net2bot(msg)
            self.__incoming_queue.put(msg)

        # blocking=False
        def pop(self):
            """ Dequeue outgoing events (framework to network) """
            msg = self.__outgoing_queue.get()
            self.__translator.bot2net(msg)
            return msg

    def __init__(self, bots):
        self.__loopback_queue = queue.Queue()
        self.__incoming_queue = queue.Queue()
        self.__outgoing_queues = dict()

    def make_endpoint(self, network, mapping=dict()):
        incoming_queue = self.__incoming_queue
        outgoing_queue = queue.Queue()
        self.__outgoing_queues[network] = outgoing_queue
        return self.Endpoint(network, incoming_queue, outgoing_queue, mapping)

    def on_schedule(self):
        instance = core.framework.Framework.get_instance()
        default_bot = instance.get_default_bot()
        user_table = instance.get_user_table()

        incoming_events = list()
        outgoing_events = list()

        while self.__loopback_queue.qsize() > 0:
            incoming_events += self.__loopback_queue.get()

        while self.__incoming_queue.qsize() > 0:
            incoming_events += self.__incoming_queue.get()

        for event in incoming_events:
            if event.category == event.Category.MESSAGE:
                bot = instance.get_bot(event.receiver)
                if bot is None:
                    bot = default_bot
                outgoing_events += bot.on_event(event)
            elif event.category == event.Category.PRESENCE_STATUS:
                user_table.on_event(event)
            else:
                logging.error('this category of event is not accepted here: {}'.format(event.category))

        for event in outgoing_events:
            if event.network == 'loopback':
                self.__loopback_queue.put(event)
            else:
                outgoing_queue = self.__outgoing_queues[event.network]
                outgoing_queue.put(event)
