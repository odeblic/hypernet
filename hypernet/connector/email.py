from core.connector import Connector
from core.message import Message
import smtplib
import time
import logging


class EMail(Connector):
    def __init__(self):
        super().__init__('email', 2, 8*1024*1024, {'bot73'   : 'bot73@hackathon.com',
                                                   'bot89'   : 'bot89@hackathon.com',
                                                   'olivier' : 'olivier@hackathon.com',
                                                   'julien'  : 'julien@hackathon.com',
                                                   })

    def _on_schedule(self):
        ret = self._pop_message_to_send()
        if ret is not None:
            logging.debug('I have to send an email')
            (message, channel) = ret
            logging.debug('{} {}'.format(channel, message))
            tokens = list()
            for element in message.find_elements():
                if isinstance(element, Message.Word):
                    tokens.append(self.make_word(element))
                elif isinstance(element, Message.Mention):
                    tokens.append(self.make_mention(element))
                elif isinstance(element, Message.Hashtag):
                    tokens.append(self.make_hashtag(element))
                elif isinstance(element, Message.Number):
                    tokens.append(self.make_number(element))
                else:
                    raise Exception('Not a valid element type')
            content = ' '.join(tokens)
            stream_id = channel.get_conversation()
            if stream_id is None:
                stream_id = 'private chat'
            sender = channel.get_sender()
            receiver = channel.get_receiver()
            conversation = 'cool'
            subject = 'Message routed by the framework for conversation {}'.format(conversation)
            body = 'Here is the original message:\n{}'.format(content)
            self.send_email(sender, receiver, subject, body)


    @staticmethod
    def make_word(text='Blablabla'):
        return '{}'.format(text)

    @staticmethod
    def make_mention(name='someone'):
        return '@{}"'.format(name)

    @staticmethod
    def make_hashtag(tag='Python37'):
        return '#{}"'.format(tag)

    @staticmethod
    def make_number(number=12345):
        return '{}"'.format(number)

    def send_email(self, sender, receiver, subject, body):
        logging.debug('I will send an email')

        if receiver is None:
            receiver = 'nobody@nowhere.com'

        email_text = "From: {}\nTo: {}\nSubject: {}\n\n{}\n".format(sender, receiver, subject, body)

        try:
            server = smtplib.SMTP('localhost', 25)
            server.ehlo()
            server.login('olivier@hackathon.com', 'xxx')
            server.sendmail(sender, receiver, email_text)
            server.quit()
            server.close()
            logging.info('the email has been sent')
        except Exception as e:
            logging.error(e)

