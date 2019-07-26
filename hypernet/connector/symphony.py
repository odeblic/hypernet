from core.channel import Channel
from core.connector import Connector
from core.message import Message

from sym_api_client_python.configure.configure import SymConfig
from sym_api_client_python.auth.rsa_auth import SymBotRSAAuth
from sym_api_client_python.clients.sym_bot_client import SymBotClient

import logging
import xml.etree.ElementTree as ET

# If the message is sent from a one to one chat, it is considered for the bot.
#
# If the message is sent from a chat room, consider it is for the bot only if it contains a mention @bot
#

class Symphony(Connector):
    _VERSION = 1

    def __init__(self):
        super().__init__()

        # stream id bnpp2019hackathon  :  'r5Z_MNRYQO5wba1iXlGyen___pU6TExodA'
        # stream id julien__bot89      :  '_wLmUVr3OQkVU1Z_5rcHxn___pU2Y8uHdA'
        # stream id olivier__bot73     :  'kq-BuonieYXqXALRDPSBAH___pUljzbbdA'
        # stream id olivier__bot89     :  'r5Z_MNRYQO5wba1iXlGyen___pU6TExodA'

        configure = SymConfig('config/bot73/rsa_config.json')
        #configure = SymConfig('config/bot89/rsa_config.json')
        configure.load_rsa_config()
        auth = SymBotRSAAuth(configure)
        auth.authenticate()

        self.bot_client = SymBotClient(auth, configure)
        self.datafeed_event_service = self.bot_client.get_datafeed_event_service()
        self.datafeed_event_service.start_datafeed('start')

        self.__private_chats = dict({'cool':'r5Z_MNRYQO5wba1iXlGyen___pU6TExodA'})

    def _on_schedule(self):
        ret = self._pop_message_to_send()
        if ret is not None:
            (message, channel) = ret
            tokens = list()
            for element in message.find_elements():
                if isinstance(element, Message.Word):
                    tokens.append(self.make_word(element))
                elif isinstance(element, Message.Mention):
                    tokens.append(self.make_mention_from_uid(element))
                elif isinstance(element, Message.Hashtag):
                    tokens.append(self.make_hashtag(element))
                elif isinstance(element, Message.Number):
                    tokens.append(self.make_number(element))
                else:
                    raise Exception('Not a valid element type')
            content = ' '.join(tokens)
            message = dict(message='<messageML><p>{}</p></messageML>'.format(content))
            stream_id = channel.get_conversation()
            if stream_id is None:
                stream_id = self.__private_chats[channel.get_receiver()]

            def set_first_mention(self, mention):
                if len(self.__elements) > 0:
                    if isinstance(self.__elements[0], Message.Mention):
                        self.__elements[0] = Message.Mention(mention)
                    else:
                        self.__elements.insert(0, Message.Mention(mention))
                else:
                    self.__elements.append(Message.Mention(mention))

            self.bot_client.get_message_client().send_msg(stream_id, message)

        data = self.datafeed_event_service.read_datafeed(self.datafeed_event_service.datafeed_id)
        if data is not None:
            events = data[0]
            for event in events:
                local_bot_id = self.bot_client.get_bot_user_info()['id']
                initiator_id = event['initiator']['user']['userId']
                if initiator_id != local_bot_id:
                    if event['type'] == 'MESSAGESENT':
                        logging.debug('Sender of message: \033[31m{}\033[0m'.format(initiator_id))
                        stream_id = event['payload']['messageSent']['message']['stream']['streamId']
                        stream_type = event['payload']['messageSent']['message']['stream']['streamType']
                        logging.debug('Stream ID: \033[33m{}\033[0m'.format(stream_id))
                        logging.debug('Type of chat: \033[33m{}\033[0m'.format(stream_type))
                        raw = event['payload']['messageSent']['message']
                        logging.debug('Message (raw event): \033[35m{}\033[0m'.format(raw))
                        presML = event['payload']['messageSent']['message']['message']
                        logging.debug('Message (PresentationML): \033[35m{}\033[0m'.format(presML))
                        xml = ET.fromstring(presML.encode('utf-8'))
                        logging.debug('Message (XML): \033[35m{}\033[0m'.format(xml))
                        plain = ET.tostring(xml, encoding='utf-8', method='text')
                        logging.info('Message (plain text): \033[35m{}\033[0m'.format(plain))

                        text = str(plain, 'utf-8')
                        text = text.replace('innovate_bot_73', 'bot73')
                        text = text.replace('innovate_bot_89', 'bot89')
                        message = Message.build(text)
                        logging.debug('Message (internal representation): \033[35m{}\033[0m'.format(message))

                        if stream_type == 'IM':
                            #self.__private_chats[initiator_id] = stream_id
                            receiver_id = local_bot_id
                        elif stream_type == 'ROOM':
                            if local_bot_id in message.find_elements(message.__class__.Mention):
                                receiver_id = local_bot_id
                            else:
                                receiver_id = None
                        else:
                            raise Exception('Invalid stream type')

                        channel = Channel(initiator_id, receiver_id, stream_id, self.get_name())
                        self._push_received_message(message, channel)

        """
        stream_id = 'kq-BuonieYXqXALRDPSBAH___pUljzbbdA'
        self.bot_client.get_message_client().send_msg(stream_id, self.make_msg_chime())
        self.bot_client.get_message_client().send_msg(stream_id, self.make_msg_with_text())
        self.bot_client.get_message_client().send_msg(stream_id, self.make_msg_with_mention_by_uid())
        self.bot_client.get_message_client().send_msg(stream_id, self.make_msg_mention_by_email())
        self.bot_client.get_message_client().send_msg(stream_id, self.make_msg_with_hashtag())
        self.bot_client.get_message_client().send_msg(stream_id, self.make_msg_with_emoticon())
        self.bot_client.get_message_client().send_msg(stream_id, self.make_msg_with_link())
        self.bot_client.get_message_client().send_msg(stream_id, self.make_msg_with_image())
        """

    @staticmethod
    def make_word(text='Blablabla'):
        return '<b class="tempo-text-color--orange">{}</b>'.format(text)

    @staticmethod
    def make_mention_from_uid(user_id):
        return '<mention uid="{}"/>'.format(user_id)

    @staticmethod
    def make_mention(name='someone'):
        return '<b class="tempo-text-color--blue">{}</b>'.format(name)

    @staticmethod
    def make_hashtag(tag='Python37'):
        return '<hash tag="{}"/>'.format(tag)

    @staticmethod
    def make_number(number=12345):
        return '<b class="tempo-text-color--red">{}</b>'.format(number)



    @staticmethod
    def make_msg_chime():
        return dict(message='<messageML><chime/></messageML>')

    @staticmethod
    def make_text2(text='No comment as long as I am paid...'):
        return dict(message="""<messageML>
                               <p>The trader likes to <b class="tempo-text-color--green">buy</b> and <b class="tempo-text-color--red">sell</b>.
                               <br/>({})</p>
                               </messageML>""".format(text))

    @staticmethod
    def make_mention_by_uid(user_id='349026222344450'):
        return dict(message='<messageML><div class="wysiwyg"><p>Hello <mention uid="{}"/>!</p></div></messageML>'.format(user_id))

    @staticmethod
    def make_mention_by_email(email='odeblic@gmail.com'):
        return dict(message='<messageML><div class="wysiwyg"><p>What\'s up <mention email="{}"/>?</p></div></messageML>'.format(email))

    @staticmethod
    def make_emoticon(shortcode='heart'):
        return dict(message='<messageML><div class="wysiwyg"><p>Romeo <emoji shortcode="{}"/> Juliet</p></div></messageML>'.format(shortcode))

    @staticmethod
    def make_link(url='https://www.dedoimedo.com/computers/dev-nonsense-netstat-ifconfig.html'):
        return dict(message='<messageML>Kindly check this <a href="{}">webpage</a>.</messageML>'.format(url))

    @staticmethod
    def make_image():
        url = 'data:image/jpeg;base64,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'
        url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT2qF1jdx2S53-qURaqKDKWL5h4TR30uxe-itrfsFmTFuu-9k5n'
        return dict(message='<messageML>Here is a nice picture<img src="{}"></img></messageML>'.format(url))

