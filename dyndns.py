#!/usr/bin/python
#
# Version OBJET
#
import re
import random
import mechanize 
from BeautifulSoup import BeautifulSoup
import socket # pour interrogation dns
import urllib # pour l'update, mechanize bug pour faire un simple get ...
import time # pour ameliorer le format de la date
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import ConfigParser

class configurationFile:
    def __init__(self):
        config = ConfigParser.RawConfigParser()
        config.read('dyndns.cfg')
        # main configuration
        self.account_file = config.get('main', 'account_file')
        self.warning_message = config.get('main','warning_message')
        self.colorize_stdout = config.get('main','colorize_stdout')

        # smtp configuration
        self.smtp_server = config.get('smtp', 'smtp_server')
        self.local_mail = config.get('smtp', 'local_mail')
        self.remote_mail = config.get('smtp', 'remote_mail')
        self.mail_subject_change_ok = config.get('smtp', 'mail_subject_change_ok')
        self.mail_subject_no_change = config.get('smtp','mail_subject_no_change')
        self.mail_subject_on_error = config.get('smtp','mail_subject_on_error')
        self.mail_text_change_ok = config.get('smtp', 'mail_text_change_ok')
        self.mail_text_no_change = config.get('smtp','mail_text_no_change')
        self.mail_text_on_error = config.get('smtp','mail_text_on_error')
        self.auto_send_mail = config.get('smtp','auto_send_mail')

class notifyBySmtp:
    def __init__(self):
        self.smtp_server = 'localhost'
        self.local_mail_address = 'toto@localhost'
        self.remote_mail_address = 'toto@gmail.com'
        self.subject = 'un sujet quoi !!!'
        self.text = 'hello'

    def setSmtpServer(self,smtpserver):
        self.smtp_server = smtpserver

    def getSmtpServer(self):
        return self.smtp_server

    def setLocalMailAddress(self,mail):
        self.local_mail_address = mail

    def getLocalMailAddress(self):
        return self.local_mail_address

    def setRemoteMailAddress(self,mail):
        self.remote_mail_address = mail

    def getLocalMailAddress(self):
        return self.local_mail_address

    def setSubject(self,subject):
        self.subject = subject

    def getSubject(self):
        return self.subject
    
    def setText(self,text):
        self.text = text

    def getText(self):
        return self.text
    
    def sendmail(self):
       # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.subject
        msg['From'] = self.local_mail_address
        msg['To'] = self.remote_mail_address

        # Record the MIME types of both parts - text/plain and text/html.
        message = MIMEText(self.text, 'plain')
        msg.attach(message)

        # Send the message via local SMTP server.
        s = smtplib.SMTP(self.smtp_server)
        s.sendmail(self.local_mail_address, self.remote_mail_address, msg.as_string())
        s.quit() 


class bcolors:
    '''

        Pour la coloration de la sortie standard.

    '''
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''

# DEBUT DE LA CLASSE
class log2dyndns(object):
    def __init__(self):
        '''

            Constructeur : permet d'initialiser certaines variables.

        '''
        self.version = '1.0'
        self.site = 'https://account.dyn.com'
        self.checkip_site = 'http://checkip.dyndns.org'

    def setAccount(self,account):
        '''

            Accepte un compte en entree et permet d'initialiser la variable account qui sera disponible a l'ensemble
            de la class via la variable self.account.

        '''
        self.account = account

    def getAccount(self):
        '''

            Cette methode permet de recuperer le contenu de la variable self.account depuis l'exterieure de la class.

        '''
        return self.account

    def setPassword(self,password):
        self.password = password

    def setSite(self,site):
        self.site = site

    def getVersion(self):
        return self.version

    def doConnect(self):
        self.br = mechanize.Browser()

        self.br.set_handle_robots(False)
        self.br.set_handle_redirect(True)
        self.br.set_handle_referer(True)
        r = self.br.open(self.site)

        counter = 0
        for form in self.br.forms():
            if "submit=Log in" in str(form):
                self.br.select_form(nr = counter)
            counter += 1

        self.br.form['username'] = self.account
        self.br.form['password'] = self.password
        self.html = self.br.submit().read()

    def doUpdate(self,dnsdomainname):
        # si changement, envoie de la modification
        # recuperation du code retour
        # si maj ok -> ok
        # si maj non ok -> authentification ?
        # si maj non ok -> je recommence 3 fois toute les 5 secondes et notification
        br = mechanize.Browser()
        r = br.open(self.checkip_site)
        html = r.read()
        current_ipaddress = re.sub(r'\n','',html)
        current_ipaddress = re.sub(r'^.*: ','',current_ipaddress)
        current_ipaddress = re.sub(r'<.*$','',current_ipaddress)
        resolv_dnsdomain = socket.gethostbyname(dnsdomainname)

        # check si on doit le faire pour ne pas incrementer le compteur 'abuse' de dyndns.org
        if current_ipaddress == resolv_dnsdomain:
            return "You don't need to update", dnsdomainname+". Your current IP address :", resolv_dnsdomain
        else:
            # ben on update
            # je dois appeler ce lien http://username:password@members.dyndns.org/nic/update?hostname=yourhostname&myip=ipaddress&wildcard=NOCHG&mx=NOCHG&backmx=NOCHG
            #link_update = "https://"+self.account+":"+self.password+"@members.dyndns.org/nic/update?hostname="+dnsdomainname+"&myip="+current_ipaddress+"&wildcard=NOCHG&mx=NOCHG&backmx=NOCHG"
            link_update = "https://"+self.account+":"+self.password+"@members.dyndns.org/nic/update?hostname="+dnsdomainname+"&myip="+current_ipaddress+"&wildcard=NOCHG&mx=NOCHG&backmx=NOCHG" 
            opener = urllib.FancyURLopener()
            code_erreur = opener.open(link_update).read()
            # la, il faut tous les tester
            # good -> ok
            # nochg -> ok mais on ne devrait jamais tomber sur cette erreur
            # notfqdn -> pas ok, la valeur du dnsdomainname n'est pas un fqdn
            # nohost -> pas ok, cas d'une faute de frappe ou d'un domain qui n'est pas sur le bon compte
            # numhost -> pas gerer, je ne comprends cette erreur
            # abuse -> pas ok du tout, le compte est bloque
            if re.search('good.*$',code_erreur):
                newip = re.sub('good ','',code_erreur)
                return "Update successfull !!! New IP address is "+newip+" for "+dnsdomainname
            elif re.search('nochg.*$',code_erreur):
                baseip = re.sub('nochg ','',code_erreur)
                return "No need to change your IP !!! Your current IP address is "+baseip+" for "+dnsdomainname
            else:
                return code_erreur

    def isConnect(self):
        check_state = "False"
        resultat = self.html.split('\n')
        regex = re.compile(r'(.*)Welcome(.*)'+self.account,re.IGNORECASE)
        for ligne in resultat: 
            if regex.match(ligne):
                check_state = "True"
                break
        return check_state

    def getState(self):
        count_host = 0  #Initialise le compteur du nombre d'hote du compte dyndns
        req = self.br.follow_link(text='My Hosts')
        data_html = req.read()

        if "No Hostnames Registered" not in data_html:
            soup = BeautifulSoup(data_html)
            table = soup.find('table', id='dyndnshostnames')
            rows = table.findAll('tr')
            list_hostname = list()

            for tr in rows:
                cols = tr.findAll('td')
                for td in cols:
                    text = td.find(text=True)
                    text2 = text.strip("\r\n")
                    text = str(text2).replace("\r"," ").replace("\n"," ").replace("\r\n"," ")
                    #print text
                    list_hostname.append(text)
                count_host += 1
            # retirer 2 au nombre d'hote compte afin d'exclure les lignes dyndns
            # hostnames et l'entete du tableau
            count_host -= 2

        # deconnexion
        self.br.follow_link(text='Log Out')
        mechanize.CookieJar.clear

        # On recupere des parametres du fichier de configuration pour influencer la sortie standard
        config = configurationFile()
        
        # Ce parametre permet d'ajuster le nombre d'espace afin d'aligner le nom du compte a droite
        # Celui-ci varie suivant l'affichage de la couleur ou pas etant donne que le calcule du positionnement
        # est fait a partir du nombre de caractere de la zone d'affichage du compte. Si celui-ci affiche
        # la couleur, le nombre de lettre affiche compte 27 lettres en plus.
        ajusteur = 27

        # Si la couleur est desactive dans le fichier de configuration, on affiche pas la couleur
        couleur = bcolors()
        if config.colorize_stdout == 'disable':
            couleur.disable()
            ajusteur = 0

        nombre_de_caracter_colonne1 = 24
        nombre_de_caracter_colonne2 = 20
        nombre_de_caracter_colonne3 = 30
        nombre_de_tiret = nombre_de_caracter_colonne1 + nombre_de_caracter_colonne2 + nombre_de_caracter_colonne3

        # affichage du nombre d'hote et de la liste de ces hotes
        reports_nbhosts = couleur.HEADER+self.account+" ["+couleur.ENDC+couleur.OKGREEN+str(count_host)+" hosts"+couleur.ENDC+couleur.HEADER+"]"+couleur.ENDC
        nombre_space = nombre_de_tiret-len(reports_nbhosts)+ajusteur
        if count_host > 0:
            print "\n"+nombre_space*" "+reports_nbhosts
        else:
            print "\n"+couleur.OKGREEN+"No hostname on "+self.account+couleur.ENDC

        reports = ""

        if count_host > 0:
            reports += couleur.OKBLUE+nombre_de_tiret*"-"+couleur.ENDC
            reports += "\n"
            reports += couleur.HEADER+'Hostname'.rjust(nombre_de_caracter_colonne1)+couleur.ENDC
            reports += couleur.HEADER+'Ip address'.rjust(nombre_de_caracter_colonne2)+couleur.ENDC
            reports += couleur.HEADER+'Last seen'.rjust(nombre_de_caracter_colonne3)+couleur.ENDC
            reports += "\n"
            reports += couleur.OKBLUE+nombre_de_tiret*"-"+couleur.ENDC
            reports += "\n"
            item = 0
            i = 0
            while item < count_host:
                hostname = list_hostname[i+1]
                ip_addr = list_hostname[i+3]
                last_seen = list_hostname[i+4]
                last_seen = time.strptime(last_seen,"%b. %d, %Y %I:%M %p")
                last_seen = time.strftime("%d/%m/%Y %H:%M",last_seen)

                reports += couleur.OKGREEN+hostname.rjust(nombre_de_caracter_colonne1)+couleur.ENDC
                reports += couleur.OKGREEN+ip_addr.rjust(nombre_de_caracter_colonne2)+couleur.ENDC
                reports += couleur.OKGREEN+last_seen.rjust(nombre_de_caracter_colonne3)+couleur.ENDC
                reports += "\n"

                i += 5
                item += 1

            reports += couleur.OKBLUE+nombre_de_tiret*"-"+couleur.ENDC
            reports += "\n"
            if config.warning_message == 'enable':
                reports += couleur.WARNING+"The default timezone is GMT+5 when you create your account for the first"+couleur.ENDC
                reports += "\n"
                reports += couleur.WARNING+"time. Configure your timezone in the preference menu on dyndns.org."+couleur.ENDC
                reports += "\n"
        return reports

# FIN DE LA CLASSE

# DEBUT DU SCRIPT
import argparse

def update_data(user,password,hostname,sendmail,local_mail,remote_mail):
    '''

        Recupere en entree le compte dyndns, le password et le nom de domaine a mettre a jour.

    '''
    myupdate = log2dyndns()
    myupdate.setAccount(user)
    myupdate.setPassword(password)
    code_erreur = myupdate.doUpdate(hostname)

    config = configurationFile()
    # On recupere la configuration du fichier de conf et on peut bypasser ce parametre par la ligne de commande
    auto_send_mail = config.auto_send_mail

    if sendmail or auto_send_mail == 'enable':
        send_email = notifyBySmtp()
        send_email.setSmtpServer(config.smtp_server)

        if local_mail == 'None' and remote_mail == 'None':
            send_email.setLocalMailAddress(config.local_mail)
            send_email.setRemoteMailAddress(config.remote_mail)
        elif local_mail == 'None' and remote_mail != 'None':
            send_email.setLocalMailAddress(config.local_mail)
            send_email.setRemoteMailAddress(remote_mail)
        elif local_mail != 'None' and remote_mail == 'None':
            send_email.setLocalMailAddress(local_mail)
            send_email.setRemoteMailAddress(config.remote_mail)
        else:    
            send_email.setLocalMailAddress(local_mail)
            send_email.setRemoteMailAddress(remote_mail)

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

        send_email.setSubject(subject)
        send_email.setText(message)
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

    laclass = log2dyndns()
    laclass.setSite('https://account.dyn.com')
    laclass.setAccount(user)
    laclass.setPassword(password)
    laclass.doConnect()

    if laclass.isConnect() == "True":
        if listing == True:
            print laclass.getState()
        else:
            print bcolors.OKGREEN+"Successfully connected with "+laclass.getAccount()+bcolors.ENDC
    else:
        print bcolors.FAIL+"Can't retrieve data with user "+laclass.getAccount()+". Wrong login or password."+bcolors.ENDC

def get_data_from_files(listing):
    '''

        Lit le fichier dyndns.conf et recurpere les couples login/password pour les envoyer a la fonction get_data.

    '''
    comptes = {}

    file = open("dyndns.conf")
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
        print bcolors.WARNING+'\n'+str(args)+bcolors.ENDC

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