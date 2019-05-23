from core.connector import Connector


class SMS(Connector):
    def __init__(self):
        super().__init__('sms', None, 512, {'007':'88446104', '9999':'87236144'})

    def _on_schedule(self):
        pass

