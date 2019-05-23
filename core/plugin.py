from abc import ABC, abstractmethod
import importlib
import inspect
import logging
import re
import sys


class Plugin(ABC):
    def __init__(self, name, version=None):
        super().__init__()
        pattern = re.compile("^[a-z][a-z0-9]+$")
        if not pattern.match(name):
            raise ValueError('Invalid plugin name')
        self.__name = name
        if version is not None and version < 1:
            raise ValueError('Invalid plugin version')
        self.__version = version

    def get_name(self):
        return self.__name

    def get_version(self):
        return self.__version

    @staticmethod
    def discover(root_package, base_class):
        plugins = dict()
        for plugin in root_package.PLUGINS:
            module = importlib.import_module(root_package.__name__ + '.' + plugin)
            for (class_name, class_type) in inspect.getmembers(sys.modules[module.__name__], inspect.isclass):
                if issubclass(class_type, base_class) and id(class_type) != id(base_class):
                    instance = class_type()
                    name = instance.get_name()
                    version = instance.get_version()
                    category = base_class.__name__.lower()
                    if version is None:
                        logging.info('Loading plugin \033[35m{}\033[0m as a \033[34m{}\033[0m'.format(name, category))
                    else:
                        logging.info('Loading plugin \033[35m{}\033[0m (version \033[35m{}\033[0m) as a \033[34m{}\033[0m'.
                            format(name, version, category))
                    plugins[name] = instance
        logging.info('Found \033[33m{}\033[0m plugin(s) of type \033[34m{}\033[0m'.
            format(len(plugins), base_class.__name__.lower()))
        return plugins

