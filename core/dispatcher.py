class Dispatcher(object):
    """ Manager responsible for delivering messages from/to the right service/agent/connector """
    def __init__(self):
        self.__queue = list()
        self.__services = list()
        self.__connectors = list()
        self.__agents = list()
        self.__bots = list()

    def on_incoming_message(self, message, channel):
        if '@globot' in message.find_elements() or channel.get_conversation() is None:
            
        else:
            pass  # message not for the bot

        # check whether the message is for the bot
        
        # search for the services involved
        
        # check the permission, basing on the roles


    def on_outgoing_message(self, message, channel):
        pass



# If the message is sent from a one to one chat, it is considered for the bot.
#
# If the message is sent from a chat room, consider it is for the bot only if it contains a mention @bot
#

