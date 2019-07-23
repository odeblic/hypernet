import pickle
import tempfile


class Cache(object):
    def __init__(self, path, content):
        self.__path = '/dev/shm/'
        # tempfile.TemporaryFile()
        self.__content = content

    def save(self):
        self = pickle.load(self.__path)

    def load(self):
        self.__content = pickle.dump(self, self.__path)

    def get(self):
        return self.__content

    def set(self, content):
        self.__content = content

