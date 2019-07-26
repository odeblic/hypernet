"""
Maintain a table of users with their details
Send presence status events on given updates
"""

import collections
import enum

User = namedtuple('User' , 'alias identifier fullname kind roles')
user = User('olivier', 'Olivier de BLIC', 'human', ['admin', 'trader', 'manager', 'dev'])


class User(collections.namedtuple('User', 'identifier kind roles statuses')):
    class Kind(enum.Enum):
        HUMAN = 1
        ROBOT = 2
        HYPERBOT = 3
        UNKNOWN = 4

    @staticmethod
    def make_human(identifier, roles=[]):
        return User(identifier, User.Kind.HUMAN, roles, {})

    @staticmethod
    def make_robot(identifier, roles=[]):
        return User(identifier, User.Kind.ROBOT, roles, {})

    @staticmethod
    def make_hyperbot(identifier, roles=[]):
        return User(identifier, User.Kind.HYPERBOT, roles, {})

    @staticmethod
    def make(identifier, kind, roles=[]):
        if kind.upper() in User.Kind:
            kind = User.Kind[kind]
            return User(identifier, kind, roles, {})
        else:
            raise


class UserTable(object):
    def __init__(self):
        self.__users = dict()
        self.__subscribers = dict()
        self.__subscribers_all = set()

    def subscribe(self, subscriber, identifiers=[]):
        for identifier in identifiers:
            if identifier not in self.__subscribers:
                self.__subscribers[identifier] = set()
            self.__subscribers[identifier].add(subscriber)

    def subscribe_all(self, subscriber):
        self.__subscribers_all.add(subscriber)

    def unsubscribe(self, subscriber, identifier=[]):
        for identifier in identifiers:
            if identifier in self.__subscribers:
                self.__subscribers[identifier].discard(subscriber)
                if len(self.__subscribers[identifier]) == 0:
                    del self.__subscribers[identifier]

    def unsubscribe_all(self, subscriber):
        self.__subscribers_all.discard(subscriber)
        for identifier, subscribers in self.__subscribers.items():
            if subscriber in subscribers:
                subscribers.discard(subscriber)
                if len(subscribers) == 0:
                    del subscribers

    def on_event(self, event):
        pass

