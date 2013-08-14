'''
    This class is used to send notification.
    - by smtp
    - by sms
    - by snmp
'''
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class NotifyBySmtp(object):
    '''
        Class NotifyBySmtp
    '''
    def __init__(self):
        self.smtp_server = ''
        self.local_mail_address = ''
        self.remote_mail_address = ''
        self.subject = ''
        self.text = ''

    def set_smtp_server(self, smtpserver):
        '''
            Set the smtp server.
        '''
        self.smtp_server = smtpserver

    def get_smtp_server(self):
        '''
            Get the smtp server.
        '''
        return self.smtp_server

    def set_sender_email(self, mail):
        '''
            Set the sender email address.
        '''
        self.local_mail_address = mail

    def get_sender_email(self):
        '''
            Get the sender email address.
        '''
        return self.local_mail_address

    def set_recipient_email(self, mail):
        '''
            Set the recipient email address.
        '''
        self.remote_mail_address = mail

    def get_recipient_email(self):
        '''
            Get the recipient email address.
        '''
        return self.remote_mail_address

    def set_subject(self, subject):
        '''
            Set the subject for the email to send.
        '''
        self.subject = subject

    def get_subject(self):
        '''
            Get the subject of the email.
        '''
        return self.subject
    
    def set_content(self, text):
        '''
            Set the email content.
        '''
        self.text = text

    def get_content(self):
        '''
            Get the content of the email.
        '''
        return self.text
    
    def sendmail(self):
        '''
            Send the mail.
        '''
       # Create message container - the correct MIME type is
       # multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.subject
        msg['From'] = self.local_mail_address
        msg['To'] = self.remote_mail_address

        # Record the MIME types of text/plain
        message = MIMEText(self.text, 'plain')
        msg.attach(message)

        # Send the message via local SMTP server.
        smtp_connect = smtplib.SMTP(self.smtp_server)
        sender = self.local_mail_address
        recipient = self.remote_mail_address
        smtp_connect.sendmail(sender, recipient, msg.as_string())
        smtp_connect.quit() 
