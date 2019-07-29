import abc
import event.event
import logging

import collections


"""
Subscriptions = collections.namedtuple('Subscription' , 'hashtags cashtags mentions')
subscriptions = Subscriptions(dict(), dict(), dict())
subscriptions = Subscriptions({1, 2, 3}, dict(), dict())

getattr(subscriptions, 'hashtags')
"""


class Subscriptions(object):
    def __init__(self):
        self.__all = set()
        self.__by_category = {
            'hashtags': dict(),
            'cashtags': dict(),
            'mentions': dict(),
            'senders': dict(),
            'receivers': dict(),
            'conversations': dict(),
            'networks': dict(),
        }

    def add(self, subscriber, *, category='all', value=None):
        if category == 'all':
            self.__all.add(subscriber)
        else:
            if value not in self.__by_category[category]:
                self.__by_category[category][value] = set()
            subscribers = self.__by_category[category][value]
            subscribers.add(subscriber)

    def remove(self, subscriber, *, category='all', value=None):
        if category == 'all':
            self.__all.discard(subscriber)
            for category, subscriptions in self.__by_category.items():
                for value in subscriptions.keys():
                    self.__by_category[category][value].discard(subscriber)
                    if len(self.__by_category[category][value]) == 0:
                        del self.__by_category[category][value]
        else:
            if value in self.__by_category[category].keys():
                self.__by_category[category][value].discard(subscriber)
                if len(self.__by_category[category][value]) == 0:
                    del self.__by_category[category][value]

    def get_subscribers(self, **kwargs):
        all_subscribers = list(self.__all)
        for category, value in kwargs.items():
            if value in self.__by_category[category]:
                all_subscribers += self.__by_category[category][value]
        return all_subscribers

    def print(self):
        print('========= all =========')
        for s in self.__all:
            print('{} -> {}'.format('all', s))
        print('========= categories =========')
        for k, v in self.__by_category.items():
            print('{} -> {}'.format(k, v))


class Bot(abc.ABC):
    def __init__(self):
        self.__subscriptions = Subscriptions()

    @abc.abstractmethod
    def get_name(self):
        pass

    def on_event(self, e):
        logging.debug('bot {} got an event: {}'.format('self.__name', event))
        if e.category == event.event.Event.Category.MESSAGE:
            msg = e.payload
            # msg.receiver
        elif e.category == event.event.Event.Category.MESSAGE:
            services = self.__subscriptions.get_subscribers()
            for service in services:
                service.on_event(e)
        else:
            logging.error('this category of event is not accepted here: {}'.format(event.category))

    def subscribe(self, subscriber, *, hashtags=[], cashtags=[], mentions=[], senders=[], receivers=[], conversations=[], networks=[]):
        for hashtag in hashtags:
            self.__subscriptions.add(subscriber, category='hashtags', value=hashtag)
        for cashtag in cashtags:
            self.__subscriptions.add(subscriber, category='cashtags', value=cashtag)
        for mention in mentions:
            self.__subscriptions.add(subscriber, category='mentions', value=mention)
        for sender in senders:
            self.__subscriptions.add(subscriber, category='senders', value=sender)
        for receiver in receivers:
            self.__subscriptions.add(subscriber, category='receivers', value=receiver)
        for conversation in conversations:
            self.__subscriptions.add(subscriber, category='conversations', value=conversation)
        for network in networks:
            self.__subscriptions.add(subscriber, category='networks', value=network)

    def subscribe_all(self, subscriber):
        self.__subscriptions.add(subscriber, category='all')

    def unsubscribe(self, subscriber, *, hashtags=[], cashtags=[], mentions=[], senders=[], receivers=[], conversations=[], networks=[]):
        for hashtag in hashtags:
            self.__subscriptions.remove(subscriber, category='hashtags', value=hashtag)
        for cashtag in cashtags:
            self.__subscriptions.remove(subscriber, category='cashtags', value=cashtag)
        for mention in mentions:
            self.__subscriptions.remove(subscriber, category='mentions', value=mention)
        for sender in senders:
            self.__subscriptions.remove(subscriber, category='senders', value=sender)
        for receiver in receivers:
            self.__subscriptions.remove(subscriber, category='receivers', value=receiver)
        for conversation in conversations:
            self.__subscriptions.remove(subscriber, category='conversations', value=conversation)
        for network in networks:
            self.__subscriptions.remove(subscriber, category='networks', value=network)

    def unsubscribe_all(self, subscriber):
        self.__subscriptions.remove(subscriber, category='all')


class NamedBot(Bot):
    def __init__(self, name):
        super().__init__()
        self.__name = name

    def get_name(self):
        return self.__name

    def send(self, channel, message):
        logging.debug('bot {} is sending to {}'.format(self.__name, channel.get_sender()))
        sender = self.__name
        receiver = channel.get_sender()
        conversation = channel.get_conversation()
        network = channel.get_network()
        return channel.__class__(sender, receiver, conversation, network)

    def reply(self, channel):
        logging.debug('bot {} is replying to {}'.format(self.__name, channel.get_sender()))
        sender = self.__name
        receiver = channel.get_sender()
        conversation = channel.get_conversation()
        network = channel.get_network()
        return channel.__class__(sender, receiver, conversation, network)

    def forward(self, channel, other_receiver, conversation=None):
        logging.debug('bot {} is forwarding to {}'.format(self.__name, other_receiver))
        sender = self.__name
        if conversation is None:
            conversation = channel.get_conversation()
        network = channel.get_network()
        return channel.__class__(sender, other_receiver, conversation, network)

    def route(self, channel, other_network):
        logging.debug('bot {} is routing between networks {} and {}'.format(self.__name, channel.get_network(), other_network))
        sender = self.__name
        receiver = channel.get_sender()
        conversation = channel.get_conversation()
        return channel.__class__(sender, receiver, conversation, other_network)


class AnonymousBot(Bot):
    def __init__(self):
        super().__init__()

    def get_name(self):
        return None
