from core.connector import Connector
import smtplib


class EMail(Connector):
    def __init__(self):
        super().__init__('email', None, 8*1024*1024, {'007':'james@mi6.en', '9999':'vlad@kgb.ru'})

    def _on_schedule(self):
        pass

    def action(self):
        gmail_user = 'you@gmail.com'  
        gmail_password = 'P@ssword!'

        sent_from = gmail_user  
        to = ['me@gmail.com', 'bill@gmail.com']  
        subject = 'OMG Super Important Message'  
        body = "Hey, what's up?\n\n- You"

        email_text = """\  
        From: %s  
        To: %s  
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_password)
            server.sendmail(sent_from, to, email_text)
            server.close()
            print('Email sent!')
        except:
            print('Something went wrong...')

