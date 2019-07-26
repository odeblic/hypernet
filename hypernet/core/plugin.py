from abc import ABC, abstractmethod
import enum
import logging
import re


class Plugin(ABC):
    def __init__(self):
        super().__init__()
        if version is None:
            logging.info('Loading plugin \033[35m{}\033[0m as a \033[34m{}\033[0m'.format(name, category))
        else:
            logging.info('Loading plugin \033[35m{}\033[0m (version \033[35m{}\033[0m) as a \033[34m{}\033[0m'.
                format(name, version, category))

        pattern = re.compile("^[a-z][a-z0-9]+$")
        if not pattern.match(name):
            raise ValueError('Invalid plugin name')
        if version is not None and version < 1:
            raise ValueError('Invalid plugin version')

    @classmethod
    def get_version(cls):
        # try except
        return cls.__module__.__version__

    @classmethod
    def get_category(cls):
        return cls.__bases__[0]


class Plugin(ABC):
    @enum.unique
    class Category(enum.Enum):
        CONNECTOR = enum.auto()
        PIPE      = enum.auto()
        SERVICE   = enum.auto()

    CATEGORY = None

    def __init__(self, name):
        super().__init__()
        # check regex name
        self.__name = name
        logging.debug('loading plugin {} of category {}'.format(self.get_name(), self.get_category()))
        self.register_plugin(self, name)

    def __del__(self):
        logging.debug('unloading plugin {} of category {}'.format(self.get_name(), self.get_category()))

    def get_category(self):
        return self.CATEGORY.name.lower()

    def get_name(self):
        return self.__name

    @staticmethod
    def register_plugin(instance, name):
        if not isinstance(instance.CATEGORY, Plugin.Category):
            logging.critical('category not defined for this plugin')

        if name in plugins[category].keys():
            logging.critical('a plugin of category {} has been already registered with name {}'.format(name, self.__category))
        else:
            plugins[category][name] = instance

