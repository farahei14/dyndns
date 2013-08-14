'''
    This class is used to parser the dyndns.cfg configuration files.
'''

import ConfigParser

class ConfigurationFile(object):
    '''
        Class ConfigurationFile
    '''
    def __init__(self):
        self.config = ''
        self.account = ''
        

    def read_configuration_file(self, files):
        '''
            Read the configuration files.
        '''
        self.config = ConfigParser.RawConfigParser()
        self.config.readfp(open(files))


    def get_main_configuration(self):
        '''
            Get the main configuration.
        '''
        return self.config.items('main')


    def get_smtp_configuration(self):
        '''
            Get the smtp configuration.
        '''
        return self.config.items('smtp')


    def read_account_file(self, account_file):
        '''
            Read the account file.
        '''
        self.account = ConfigParser.RawConfigParser()
        self.account.readfp(open(account_file))


    def get_account(self):
        '''
            Get the account data.
        '''
        return self.account.items('account')