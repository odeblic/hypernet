from core.connector import Connector


class RESTful(Connector):
    def __init__(self):
        super().__init__('restful', None, 1024, {'007':'James Bond', '9999':'V. Poutine'})

    def _on_schedule(self):
        pass

