from core.connector import Connector


class RESTful(Connector):
    def __init__(self):
        super().__init__()

    def _on_schedule(self):
        pass

"""

get_swagger
  yaml file

list_users
  name
  kind
  role

send_message
  recipient
  conversation
  message

receive_message

"""

