import bidict


class Translator(object):
    class Map(object):
        def __init__(self):
            self.__map = bidict.bidict()

        def add_id_pair(self, bot_id, net_id):
            if self.__is_bot_id(bot_id):
                raise Exception('This identifier is already used within the bot framework')
            if self.__is_net_id(net_id):
                raise Exception('This identifier is already used within the network')
            else:
                self.__map[bot_id] = net_id

        def bot2net(self, bot_id):
            if bot_id is None: return None
            if not self.__is_bot_id(bot_id):
               raise Exception('This identifier does not exist')
            return self.__map[bot_id]

        def net2bot(self, net_id):
            if net_id is None: return None
            if not self.__is_net_id(net_id):
               self.__allocate_id(net_id)
            return self.__map.inverse[net_id]

        def __is_bot_id(self, bot_id):
            return bot_id in self.__map.keys()

        def __is_net_id(self, net_id):
            return net_id in self.__map.values()

        def __allocate_id(self, net_id):
            counter = 0
            while True:
                counter += 1
                bot_id = 'unknown{}'.format(counter)
                if not self.__is_bot_id(bot_id):
                    self.add_id_pair(bot_id, net_id)
                    return bot_id

    def __init__(self):
        self.__agents = self.Map()
        self.__conversations = self.Map()

    def add_agent(self, bot_id, net_id):
        self.__agents.add_id_pair(bot_id, net_id)

    def add_conversation(self, bot_id, net_id):
        self.__conversations.add_id_pair(bot_id, net_id)

    def bot2net(self, channel):
        snd_bot_id = channel.get_sender()
        rcv_bot_id = channel.get_receiver()
        con_bot_id = channel.get_conversation()

        snd_net_id = self.__agents.bot2net(snd_bot_id)
        rcv_net_id = self.__agents.bot2net(rcv_bot_id)
        con_net_id = self.__conversations.bot2net(con_bot_id)

        return channel.__class__(snd_net_id,
                                 rcv_net_id,
                                 con_net_id)

    def net2bot(self, channel):
        snd_net_id = channel.get_sender()
        rcv_net_id = channel.get_receiver()
        con_net_id = channel.get_conversation()

        snd_bot_id = self.__agents.net2bot(snd_net_id)
        rcv_bot_id = self.__agents.net2bot(rcv_net_id)
        con_bot_id = self.__conversations.net2bot(con_net_id)

        return channel.__class__(snd_bot_id,
                                 rcv_bot_id,
                                 con_bot_id)

