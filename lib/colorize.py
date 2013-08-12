class BColors(object):
    '''
        Pour la coloration de la sortie standard.
    '''
    header = '\033[95m'
    okblue = '\033[94m'
    okgreen = '\033[92m'
    warning = '\033[93m'
    fail = '\033[91m'
    endc = '\033[0m'

    def disable(self):
        '''
            Disable the color scheme.
        '''
        self.header = ''
        self.okblue = ''
        self.okgreen = ''
        self.warning = ''
        self.fail = ''
        self.endc = ''