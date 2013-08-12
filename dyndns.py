#!/usr/bin/python
#
from lib.notify import NotifyBySmtp
from lib.configuration import ConfigurationFile
from lib.colorize import BColors
from lib.log2dyndns import Log2DynDns

import argparse

def update_data(user,password,hostname,sendmail,local_mail,remote_mail):
    '''

        Recupere en entree le compte dyndns, le password et le nom de domaine a mettre a jour.

    '''
    myupdate = Log2DynDns()
    myupdate.set_account(user)
    myupdate.set_password(password)
    code_erreur = myupdate.do_update(hostname)

    config = ConfigurationFile()
    # On recupere la configuration du fichier de conf et on peut bypasser ce parametre par la ligne de commande
    auto_send_mail = config.auto_send_mail

    if sendmail or auto_send_mail == 'enable':
        send_email = NotifyBySmtp()
        send_email.set_smtp_server(config.smtp_server)

        if local_mail == 'None' and remote_mail == 'None':
            send_email.set_sender_email(config.local_mail)
            send_email.set_recipient_email(config.remote_mail)
        elif local_mail == 'None' and remote_mail != 'None':
            send_email.set_sender_email(config.local_mail)
            send_email.set_recipient_email(remote_mail)
        elif local_mail != 'None' and remote_mail == 'None':
            send_email.set_sender_email(local_mail)
            send_email.set_recipient_email(config.remote_mail)
        else:    
            send_email.set_sender_email(local_mail)
            send_email.set_recipient_email(remote_mail)

        if re.search('Update successfull.*$',code_erreur):
            subject = config.mail_subject_change_ok
            message = config.mail_text_change_ok
        elif re.search('No need.*$',code_erreur):
            subject = config.mail_subject_no_change
            message = config.mail_text_no_change
        else:
            subject = config.mail_subject_on_error
            message = config.mail_text_on_error

        # je n'ai pas l'adresse ip, je dois la calculer a partir du code d'erreur
        ip_addr = re.sub(r'^.* is ','',code_erreur)
        ip_addr = re.sub(r' for.*$','',ip_addr)

        # prise en compte des templates
        subject = re.sub(r'{hostname}',hostname,subject)
        subject = re.sub(r'{ip}',ip_addr,subject)
        message = re.sub(r'{hostname}',hostname,message)
        message = re.sub(r'{ip}',ip_addr,message)
        message = re.sub(r'\\n','\n',message)
        message = message+"\n\nLog :\n"+code_erreur

        send_email.set_subject(subject)
        send_email.set_content(message)
        send_email.sendmail()

    print code_erreur

def get_data(user,password,listing):
    '''

        Recupere en entree le compte dydns, le password et le parametre listing (qui permet de lancer la procedure de listing ou pas).

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

    bcolors = BColors

    if laclass.isConnect() == "True":
        if listing == True:
            print laclass.getState()
        else:
            print bcolors.okgreen+"Successfully connected with "+laclass.get_account()+bcolors.endc
    else:
        print bcolors.FAIL+"Can't retrieve data with user "+laclass.get_account()+". Wrong login or password."+bcolors.endc

def get_data_from_files(listing):
    '''

        Lit le fichier dyndns.conf et recurpere les couples login/password pour les envoyer a la fonction get_data.

    '''
    comptes = {}

    file = open("etc/dyndns.conf")
    while 1:
        lines = file.readlines(100000)
        if not lines:
            break
        for line in lines:
            # je passe les lignes de commentaires du fichier de parametre
            if re.search('^#.*$',line):
                continue
            # je passe les lignes vides
            if re.search('^\n',line):
                continue
            account = re.sub(':.*','',line)
            account = re.sub(r'\'','',account)
            account = re.sub(r'\n','',account)
            password = re.sub('^.*:','',line)
            password = re.sub(r'\'','',password)
            password = re.sub(r'\n','',password)
            comptes[account] = password
    for compte, password in comptes.items():
        get_data(compte,password,listing)

def debug_mode(args):
    if args.debug_mode:
        print bcolors.WARNING+'\n'+str(args)+bcolors.endc

def print_authentication(subparsers):
    subparsers.add_argument('-u', dest='username', action='store', help='dyndns account', default='None')
    subparsers.add_argument('-p', dest='password', action='store', help='dyndns account password', default='None')

def main():
    '''

        La fonction principale permet d'aiguiller les options de la ligne de commande aux fonctions intermediaires.

    '''
    parser = argparse.ArgumentParser(add_help=True,description='Manage your Dyndns Account.')
    
    # Options globales
    parser.add_argument('--all', dest='all', action='store_true', help='Options for all account', default=False)
    parser.add_argument('--debug', dest='debug_mode', action='store_true', help='Debug mode', default=False)

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
    update.add_argument('-H', dest='hostname', action='store', help='dyndns hostname', default='None')

    # Mettre ces parametres dans le fichier de configuration
    update.add_argument('--notify', dest='sendmail', action='store_true', help='notify by mail', default=False)
    update.add_argument('--local_mail', dest='local_mail', action='store', help='sender email address', default='None')
    update.add_argument('--remote_mail', dest='remote_mail', action='store', help='recipient email address', default='None')

    args = parser.parse_args()

    if args.all == True and args.name != 'update':
        debug_mode(args)
        get_data_from_files(args.name)
    elif args.all == True and args.name == 'update':
        debug_mode(args)
        print "Can't do that ..."
    elif args.all == False and args.name == 'update':
        debug_mode(args)
        update_data(args.username,args.password,args.hostname,args.sendmail,args.local_mail,args.remote_mail)
    else:
        debug_mode(args)
        get_data(args.username,args.password,args.name)


if __name__ == "__main__":
    main()