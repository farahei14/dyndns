'''
    tsss
'''
import re
import mechanize
from mechanize import Browser
from BeautifulSoup import BeautifulSoup
import socket # pour interrogation dns
import urllib # pour l'update, mechanize bug pour faire un simple get ...
import time # pour ameliorer le format de la date

class Log2DynDns(object):
    '''
        Class Log2DynDns
        Example :
            object = Log2DynDns()
            object.set_account(dyndns_account)
            object.set_password(dyndns_password)
            object.do_connect()
    '''
    def __init__(self):
        '''
            Log2DynDns constructor.
        '''
        self.account_site = 'https://account.dyn.com'
        self.checkip_site = 'http://checkip.dyndns.org'
        self.account = ''
        self.password = ''
        self.mechanize_object = Browser()
        self.html = ''


    def set_account(self, account):
        '''
            Set the dyndns account.
        '''
        self.account = account


    def get_account(self):
        '''
            Return the password.
        '''
        return self.account


    def set_password(self, password):
        '''
            Set the password.
        '''
        self.password = password


    def set_site(self, site):
        '''
            Set the website of dyndns.
        '''
        self.account_site = site


    def do_connect(self):
        '''
            Connect to dyndns website and log in with an account.
        '''
        self.mechanize_object.set_handle_robots(False)
        self.mechanize_object.set_handle_redirect(True)
        self.mechanize_object.set_handle_referer(True)
        self.mechanize_object.open(self.account_site)

        counter = 0

        for form in self.mechanize_object.forms():
            if "submit=Log in" in str(form):
                self.mechanize_object.select_form(nr = counter)
            counter += 1

        self.mechanize_object.form['username'] = self.account
        self.mechanize_object.form['password'] = self.password
        self.html = self.mechanize_object.submit().read()


    def do_update(self, dnsdomainname):
        '''
            Update dyndns hostname.
        '''
        # si changement, envoie de la modification
        # recuperation du code retour
        # si maj ok -> ok
        # si maj non ok -> authentification ?
        # si maj non ok -> je recommence 3 fois toute les 5 secondes et
        # notification
        br_test = Browser()
        r = br_test.open(self.checkip_site)
        html = r.read()
        current_ipaddress = re.sub(r'\n', '', html)
        current_ipaddress = re.sub(r'^.*: ', '', current_ipaddress)
        current_ipaddress = re.sub(r'<.*$', '', current_ipaddress)
        resolv_dnsdomain = socket.gethostbyname(dnsdomainname)

        # check si on doit le faire pour ne pas incrementer le compteur
        # 'abuse' de dyndns.org
        if current_ipaddress == resolv_dnsdomain:
            return "You don't need to update", dnsdomainname+". Your current IP address :", resolv_dnsdomain
        else:
            # ben on update
            # je dois appeler ce lien http://username:password@members.dyndns.o
            # rg/nic/update?hostname=yourhostname&myip=ipaddress&wildcard=NOCHG
            # &mx=NOCHG&backmx=NOCHG
            #link_update = "https://"+self.account+":"+self.password+"@members.
            #dyndns.org/nic/update?hostname="+dnsdomainname+"&myip="+current_ip
            #address+"&wildcard=NOCHG&mx=NOCHG&backmx=NOCHG"

            link_update = "https://"+self.account+":"+self.password+"@members.dyndns.org/nic/update?hostname="+dnsdomainname+"&myip="+current_ipaddress+"&wildcard=NOCHG&mx=NOCHG&backmx=NOCHG" 
            opener = urllib.FancyURLopener()
            code_erreur = opener.open(link_update).read()
            # la, il faut tous les tester
            # good -> ok
            # nochg -> ok mais on ne devrait jamais tomber sur cette erreur
            # notfqdn -> pas ok, la valeur du dnsdomainname n'est pas un fqdn
            # nohost -> pas ok, cas d'une faute de frappe ou d'un domain qui
            # n'est pas sur le bon compte
            # numhost -> pas gerer, je ne comprends cette erreur
            # abuse -> pas ok du tout, le compte est bloque

            if re.search('good.*$', code_erreur):
                newip = re.sub('good ', '', code_erreur)
                return "Update successfull !!! New IP address is "+newip+" for "+dnsdomainname
            elif re.search('nochg.*$', code_erreur):
                baseip = re.sub('nochg ', '', code_erreur)
                return "No need to change your IP !!! Your current IP address is "+baseip+" for "+dnsdomainname
            else:
                return code_erreur


    def is_connect(self):
        '''
            tsss
        '''
        check_state = "False"
        resultat = self.html.split('\n')
        regex = re.compile(r'(.*)Welcome(.*)'+self.account, re.IGNORECASE)
        for ligne in resultat: 
            if regex.match(ligne):
                check_state = "True"
                break
        return check_state


    def get_hosts(self):
        '''
            Get state.
        '''
        req = self.mechanize_object.follow_link(text='My Hosts')
        data_html = req.read()

        if "No Hostnames Registered" not in data_html:
            soup = BeautifulSoup(data_html)
            table = soup.find('table', id='dyndnshostnames')
            rows = table.findAll('tr')
            list_host = list()

            for tr in rows:
                cols = tr.findAll('td')

                # transformation
                info = re.sub(r'\r', ' ', str(cols))
                info = re.sub(r'\r\n', ' ', info)
                info = re.sub(r'\n', ' ', info)
                info = re.sub(r'<td>', '', info)
                info = re.sub(r'</td>', '', info)
                info = re.sub(r'<td.*id">', '', info)
                info = re.sub(r'<a .*.org">', '', info)
                info = re.sub(r'</a>', '', info)
                info = re.sub(r'<td.*t , ', '', info)
                info = re.sub(r'\[', '', info)
                info = re.sub(r'\]', '', info)
                
                if info == '':
                    pass
                else:
                    info = tuple(info.split(', '))
                    data = info[0]+','+info[1]+','+info[2]
                    last_seen = info[3]+' '+info[4]
                    last_seen = time.strptime(last_seen,"%b. %d %Y %I:%M %p")
                    last_seen = time.strftime("%m/%d/%Y %H:%M", last_seen)
                    merge = data+','+last_seen
                    info = tuple(merge.split(','))
                    list_host.append(info)

        # deconnexion
        self.mechanize_object.follow_link(text='Log Out')
        mechanize.CookieJar.clear

        print list_host
        return list_host

