import logging
import hypernet

__version__ = 1


class Main(hypernet.Connector):
    def __init__(self, arguments, handler):
        super().__init__()

