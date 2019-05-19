class Channel(object):
    """ Identifiers of entities involved in a message """
    def __init__(self, sender, receiver, conversation):
        self.__sender = sender
        self.__receiver = receiver
        self.__conversation = conversation
        if not self.is_valid():
            raise Exception('Invalid channel')

    def is_valid(self):
        if self.__sender is None:
            return False
        elif self.__receiver is None and self.__conversation is None:
            return False
        else:
            return True

    def set_local_agent(self, local_agent):
        self.__class__.__local_agent = local_agent

    def get_local_agent(self):
        return self.__class__.__local_agent

    def get_sender(self):
        return self.__sender

    def get_receiver(self):
        return self.__receiver

    def get_conversation(self):
        return self.__conversation

    def reply(self):
        sender = self.get_local_agent()
        receiver = self.__sender
        return self.__class__(sender, receiver, self.__conversation)

    def forward(self, remote_agent, conversation=None):
        sender = self.get_local_agent()
        receiver = remote_agent
        if conversation is None:
            conversation = self.__conversation
        return self.__class__(sender, receiver, conversation)

