import bidict


class Translator(object):
    def __init__(self, mapping=dict()):
        self.__mapping = bidict.bidict(mapping)

    def add_id_pair(self, bot_id, net_id):
        if self.is_bot_id(bot_id):
            raise Exception('This identifier is already used within the framework')
        if self.is_net_id(net_id):
            raise Exception('This identifier is already used within the network')
        else:
            self.__mapping[bot_id] = net_id

    def is_bot_id(self, bot_id):
        return bot_id in self.__mapping.keys()

    def is_net_id(self, net_id):
        return net_id in self.__mapping.values()

    def allocate(self, net_id):
        counter = 0
        while True:
            counter += 1
            bot_id = 'unknown{}'.format(counter)
            if not self.is_bot_id(bot_id):
                self.add_id_pair(bot_id, net_id)
                return bot_id

    def bot2net(self, bot_id):
        return self.__mapping[bot_id]

    def net2bot(self, net_id):
        return self.__mapping.inverse[net_id]

