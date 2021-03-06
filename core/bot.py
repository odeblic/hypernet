import logging
from core.plugin import Plugin


def load_services():
    import services
    from core.service import Service
    return Plugin.discover(services, Service)


class Bot(object):
    def __init__(self, name):
        self.__name = name
        self.__services = load_services()
        for service in self.__services.values():
            service._bot = self

    def get_name(self):
        return self.__name

    def deliver_incoming_message(self, message, channel):
        #logging.debug('deliver_incoming_messages(...) for bot \033[32m{}\033[0m'.format(self.__name))
        dispatched = False
        for element in message.find_elements(message.__class__.Hashtag):
            for name, service in self.__services.items():
                if service.get_name() == element:
                    logging.debug('dispatched to service \033[32m{}\033[0m'.format(service.get_name()))
                    service.deliver_incoming_message(message, channel)
                    dispatched = True
        if not dispatched:
            logging.debug('no dispatching (no matching service)')

    def on_schedule(self):
        #logging.debug('on_schedule(...) for bot \033[32m{}\033[0m'.format(self.__name))
        for service in self.__services.values():
            service.on_schedule()

    def fetch_outgoing_messages(self):
        #logging.debug('fetch_outgoing_messages(...) for bot \033[32m{}\033[0m'.format(self.__name))
        outgoing_messages = list()
        for service in self.__services.values():
            while True:
                ret = service.fetch_outgoing_message()
                if ret is None: break
                outgoing_messages.append(ret)
        return outgoing_messages

    def reply(self, channel):
        sender = self.__name
        receiver = channel.get_sender()
        conversation = channel.get_conversation()
        network = channel.get_network()
        return channel.__class__(sender, receiver, conversation, network)

    def forward(self, remote_agent, conversation=None):
        sender = self.__name
        receiver = remote_agent
        if conversation is None:
            conversation = channel.get_conversation()
        network = channel.get_network()
        return channel.__class__(sender, receiver, conversation, network)

    def route(self, network):
        pass

