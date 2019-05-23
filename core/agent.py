from enum import Enum


class Agent(object):
    class Category(Enum):
        MYSELF = 1
        ROBOT  = 2
        HUMAN  = 3

    class Role(Enum):
        ADMIN = 1
        USER  = 2
        GUEST = 3

    def __init__(self, identifier, category, role=None):
        self.__identifier = identifier
        self.__category = category
        self.__role = role

