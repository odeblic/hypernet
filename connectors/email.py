from core.connector import Connector
import smtplib
import time
import logging


class EMail(Connector):
    def __init__(self):
        super().__init__('email', 2, 8*1024*1024, {'007':'james@mi6.en', '9999':'vlad@kgb.ru'})

    def _on_schedule(self):
        time.sleep(4)
        self.send_email('I want to test this email sender')

    def send_email(self, body):
        logging.debug('I send an email')
        sent_from = 'olivier@hackathon.com'
        to = ['olivier@hackathon.com']  
        subject = 'Message routed from the framework'

        email_text = """From: %s
To: %s
Subject: %s

%s
        """ % (sent_from, ", ".join(to), subject, body)
        try:
            logging.debug('I connect')
            #server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server = smtplib.SMTP('localhost', 25)
            logging.debug('I say hello')
            server.ehlo()
            logging.debug('I log in')
            server.login('olivier@hackathon.com', 'xxx')
            logging.debug('I send the email')
            server.sendmail('olivier@hackathon.com', 'olivier@hackathon.com', email_text)
            logging.debug('I quit')
            server.quit()
            logging.debug('I close')
            server.close()
            logging.info('Email sent!')
        except:
            logging.error('Something went wrong...')
            