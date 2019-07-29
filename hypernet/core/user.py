"""
Maintain a table of users with their details
Send presence status events on given updates
"""

import collections
import event as evt
import enum
import logging


class User(collections.namedtuple('User', 'identifier kind roles statuses')):
    class Kind(enum.Enum):
        UNKNOWN = 0
        HUMAN = 1
        ROBOT = 2
        HYPERBOT = 3

    @classmethod
    def make_human(cls, identifier, roles=None):
        return cls.make(identifier, User.Kind.HUMAN, roles)

    @classmethod
    def make_robot(cls, identifier, roles=None):
        return cls.make(identifier, User.Kind.ROBOT, roles)

    @classmethod
    def make_hyperbot(cls, identifier, roles=None):
        return cls.make(identifier, User.Kind.HYPERBOT, roles)

    @classmethod
    def make(cls, identifier, kind, roles=None):
        if roles is None:
            roles = []
            return cls(identifier, kind, roles, dict())
        else:
            raise

    @classmethod
    def get_kind(cls, kind):
        if kind.upper() in cls.Kind:
            return cls.Kind[kind.upper()]
        else:
            logging.error('Invalid kind of user: {}'.format(kind))
            return cls.Kind.UNKNOWN


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
        print(event)
        if event.category == evt.event.Event.Category.USER_DISCOVERY:
            self.__users[event.payload.framework_id] = dict()
            self.__users[event.payload.framework_id]['identifier'] = event.payload.framework_id
            self.__users[event.payload.framework_id]['kind'] = event.payload.kind
            self.__users[event.payload.framework_id]['roles'] = event.payload.roles
