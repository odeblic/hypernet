"""Generic class to be extended to implement a service"""

from abc import abstractmethod


class Service(Plugin):
    def __init__(self, name):
        super().__init__()
        self.__name = name

    def get_name(self):
        return self.__name

    @abstractmethod
    def on_event(self, event):
        pass

    def list_components(self, category):
        self.__objects[category]




from collections import namedtuple

Framework = namedtuple('Framework', 'users networks bots services statistics')

networks = list('symphony', 'email', 'facebook')
networks = set(networks)

framework = Framework(users, networks, bots, services, statistics)


core.py
    usertable  presence_status, new_user
    networks
    connectors
    bots
    services
    clock
    dispatcher

    def get_users()
        pass

    def get_clock()
        pass

    def get_dispatcher()
        pass

    def get_clock()
        pass

