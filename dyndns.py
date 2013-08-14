#!/usr/bin/python
'''
    Ce script permet de manager vos comptes dyndns.
'''
from lib.notify import NotifyBySmtp
from lib.configuration import ConfigurationFile
from lib.colorize import BColors
from lib.log2dyndns import Log2DynDns

import argparse
import re

def update_data(user, password, hostname):
    '''
        Update ip address for a dyndns host.
    '''
    myupdate = Log2DynDns()
    myupdate.set_account(user)
    myupdate.set_password(password)
    code_erreur = myupdate.do_update(hostname)

    config = ConfigurationFile()
    config.read_configuration_file('etc/dyndns.cfg')
    k = dict(config.get_smtp_configuration())

    if k['auto_send_mail'] == 'enable':
        if re.search('Update successfull.*$', code_erreur):
            subject = k['mail_subject_change_ok']
            message = k['mail_text_change_ok']
        elif re.search('No need.*$', code_erreur):
            subject = k['mail_subject_no_change']
            message = k['mail_text_no_change']
        else:
            subject = k['mail_subject_on_error']
            message = k['mail_text_on_error']

        # je n'ai pas l'adresse ip, je dois la calculer a partir du code
        # d'erreur
        ip_addr = re.sub(r'^.* is ', '', code_erreur)
        ip_addr = re.sub(r' for.*$', '', ip_addr)

        # prise en compte des templates
        subject = re.sub(r'{hostname}', hostname, subject)
        subject = re.sub(r'{ip}', ip_addr, subject)
        message = re.sub(r'{hostname}', hostname, message)
        message = re.sub(r'{ip}', ip_addr, message)
        message = re.sub(r'\\n', '\n', message)
        message = message+"\n\nLog :\n"+code_erreur

        send_email = NotifyBySmtp()
        send_email.set_smtp_server(k['smtp_server'])
        send_email.set_sender_email(k['local_mail'])
        send_email.set_recipient_email(k['remote_mail'])
        send_email.set_subject(subject)
        send_email.set_content(message)
        send_email.sendmail()
    print code_erreur


def get_data(user, password, listing):
    '''
        Get data from a dyndns account.
    '''
    if listing == 'list':
        listing = True
    else:
        listing = False

    laclass = Log2DynDns()
    laclass.set_site('https://account.dyn.com')
    laclass.set_account(user)
    laclass.set_password(password)
    laclass.do_connect()

    config = ConfigurationFile()
    config.read_configuration_file('etc/dyndns.cfg')
    k = dict(config.get_main_configuration())

    couleur = BColors()
    if k['colorize_stdout'] == 'disable':
        couleur.disable()

    if laclass.is_connect() == "True":
        if listing == True:
            print laclass.get_state()
        else:
            mess = "Successfully connected with "
            print couleur.okgreen+mess+laclass.get_account()+couleur.endc
    else:
        mess = "Can't retrieve data with user "
        mess2 = ". Wrong login or password."
        print couleur.fail+mess+laclass.get_account()+mess2+couleur.endc


def get_data_from_files(listing):
    '''
        Get data for all dydns account based on your configuration file.
    '''
    accounts = ConfigurationFile()
    accounts.read_account_file('etc/dyndns.conf')
    for compte, password in accounts.get_account():
        get_data(compte, password, listing)


def debug_mode(args):
    '''
        Active debug mode when needed.
    '''
    if args.debug_mode:
        bcolors = BColors
        print bcolors.warning+'\n'+str(args)+bcolors.endc


def print_authentication(subparsers):
    '''
        Add subparser for user/password to any parser who need it.
    '''    
    subparsers.add_argument('-u', dest='username', action='store',
        help='dyndns account', default='None')
    subparsers.add_argument('-p', dest='password', action='store',
        help='dyndns account password', default='None')


def main():
    '''
        Main function.
    '''
    parser = argparse.ArgumentParser(add_help=True, 
        description='Manage your Dyndns Account.')
    
    # Options globales
    parser.add_argument('--all', dest='all', action='store_true',
        help='Options for all account', default=False)
    parser.add_argument('--debug', dest='debug_mode', action='store_true',
        help='Debug mode', default=False)

    # Creation des subparsers
    subparsers = parser.add_subparsers(dest='name')

    # Connect only
    connect = subparsers.add_parser('connect', help='connect hostnames')
    print_authentication(connect)

    # List hostname
    listing = subparsers.add_parser('list', help='listing hostnames')
    print_authentication(listing)

    # Update hostname
    update = subparsers.add_parser('update', help='update hostnames')
    print_authentication(update)
    update.add_argument('-H', dest='hostname', action='store',
        help='dyndns hostname', default='None')

    args = parser.parse_args()

    if args.all == True and args.name != 'update':
        debug_mode(args)
        get_data_from_files(args.name)
    elif args.all == True and args.name == 'update':
        debug_mode(args)
        print "Can't do that ..."
    elif args.all == False and args.name == 'update':
        debug_mode(args)
        update_data(args.username, args.password, args.hostname)
    else:
        debug_mode(args)
        get_data(args.username, args.password, args.name)


if __name__ == "__main__":
    main()