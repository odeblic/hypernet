import glob
import os

def plugin_discovery():
    files = glob.glob('{}/*.py'.format(os.path.dirname(__file__)))
    modules = list()
    for f in files:
        path = os.path.splitext(f)[0]
        module = os.path.basename(path)
        if module != '__init__':
            modules.append(module)
    return set(modules)


PLUGINS = plugin_discovery()

