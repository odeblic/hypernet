class Channel(object):
    """ Identifiers of entities involved in a message """
    def __init__(self, sender, receiver, conversation, network):
        self.__sender = sender
        self.__receiver = receiver
        self.__conversation = conversation
        self.__network = network
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

    def get_network(self):
        return self.__network

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

    def __str__(self):
        sender = self.get_sender()
        receiver = self.get_receiver()
        conversation = self.get_conversation()
        if sender is not None:
            sender_section = 'from \033[33m{}\033[0m'.format(sender)
        else:
            sender_section = 'from \033[36many\033[0m'
        if receiver is not None:
            receiver_section = ' to \033[33m{}\033[0m'.format(receiver)
        else:
            receiver_section = ' to \033[36many\033[0m'
        if conversation is not None:
            conversation_section = ' in chatroom \033[31m{}\033[0m'.format(conversation)
        else:
            conversation_section = ' in private chat'
        network_section = ' on network \033[34m{}\033[0m'.format(self.get_network())
        return '{}{}{}{}'.format(sender_section, receiver_section, conversation_section, network_section)

