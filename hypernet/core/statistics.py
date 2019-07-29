"""Send tick events on given times"""


class Statistics(object):
    def __init__(self):
        self.__dropped = 0
        self.__ignored = 0
        self.__incoming = 0
        self.__outgoing = 0
        # latency
        # message rate
        self.__load_factor = None
        self.__load_factor = 0

    def add_dropped(self, count=1):
        self.__dropped += count

    def add_ignored(self, count=1):
        self.__ignored += count

    def get_dropped(self):
        return self.__dropped

    def get_ignored(self):
        return self.__ignored
