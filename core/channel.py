class Channel(object):
    """ Identifiers of entities involved in a message to ensure its delivery """
    def __init__(self, sender, receiver, conversation, network):
        if sender is None:
            raise Exception('A channel must have a sender')
        elif receiver is None and conversation is None:
            raise Exception('A channel must have either a receiver or a conversation')
        self.__sender = sender
        self.__receiver = receiver
        self.__conversation = conversation
        self.__network = network

    def get_sender(self):
        return self.__sender

    def get_receiver(self):
        return self.__receiver

    def get_conversation(self):
        return self.__conversation

    def get_network(self):
        return self.__network

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

