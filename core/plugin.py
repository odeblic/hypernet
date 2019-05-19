import importlib
import inspect
import sys


class Plugin(object):
    def __init__(self, name=None):
        self.__name = name

    def get_name(self):
        return self.__name

    @staticmethod
    def discover(root_package, base_class):
        plugins = list()
        for plugin in root_package.PLUGINS:
            module = importlib.import_module(root_package.__name__ + '.' + plugin)
            classes = list()
            for c in inspect.getmembers(sys.modules[module.__name__], inspect.isclass):
                class_name = c[0]
                class_type = c[1]
                if issubclass(class_type, base_class) and id(class_type) != id(base_class):
                    print('Loading plugin \033[35m{}\033[0m as a \033[34m{}\033[0m'.format(class_name.lower(), base_class.__name__.lower()))
                    classes.append('\033[32m{}\033[0m'.format(class_name))
                    plugins.append(class_type)
                else:
                    classes.append('\033[31m{}\033[0m'.format(class_name))
        print('Found \033[33m{}\033[0m plugin(s) of type \033[34m{}\033[0m'.format(len(plugins), base_class.__name__.lower()))
        return plugins

