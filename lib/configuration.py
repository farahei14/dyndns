'''
    This class is used to parser the dyndns.cfg configuration files.
'''

import ConfigParser

class ConfigurationFile():
    '''
        Class ConfigurationFile
    '''
    def __init__(self):
        self.config = ConfigParser.RawConfigParser()
        self.account_file = ''
        self.warning_message = ''
        self.colorize_stdout = ''
        self.smtp_server = ''
        self.sender_email = ''
        self.recipient_email = ''
        self.mail_subject_change_ok = ''
        self.mail_subject_no_change = ''
        self.mail_subject_on_error = ''
        self.mail_text_change_ok = ''
        self.mail_text_no_change = ''
        self.mail_text_on_error = ''
        self.auto_send_mail = ''

    def read_configuration_file(self):
        '''
            Read the configuration files.
        '''
        self.config.read('dyndns.cfg')

    def get_main_configuration(self):
        '''
            Get the main configuration.
        '''
        self.account_file = self.config.get('main', 'account_file')
        self.warning_message = self.config.get('main','warning_message')
        self.colorize_stdout = self.config.get('main','colorize_stdout')        
    def get_smtp_configuration(self):
        '''
            Get the smtp configuration.
        '''
        self.smtp_server = self.config.get('smtp', 'smtp_server')
        self.sender_email = self.config.get('smtp', 'local_mail')
        self.recipient_email = self.config.get('smtp', 'remote_mail')
        self.mail_subject_change_ok = \
        self.config.get('smtp', 'mail_subject_change_ok')
        self.mail_subject_no_change = \
        self.config.get('smtp','mail_subject_no_change')
        self.mail_subject_on_error = \
        self.config.get('smtp','mail_subject_on_error')
        self.mail_text_change_ok = \
        self.config.get('smtp', 'mail_text_change_ok')
        self.mail_text_no_change = \
        self.config.get('smtp','mail_text_no_change')
        self.mail_text_on_error = self.config.get('smtp','mail_text_on_error')
        self.auto_send_mail = self.config.get('smtp','auto_send_mail')

