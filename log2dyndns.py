#!/usr/bin/python
# -*- coding: utf-8 -*-
# Script de mise à jour du compte dyndns
# Nécessite le module :
# - python-mechanize
# - beautifulsoup

import mechanize 
from BeautifulSoup import BeautifulSoup
import re
import random

username = ['account']
password = 'password'
page_home = 'https://account.dyn.com'
page_myhosts = 'My Hosts'

# Fonction log2dyndns
# Connexion sur le site dyndns
def log2dyndns(pageweb,identifiant,mot2passe):
	fake_agent = [
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36',
	    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0',
	    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.110 Safari/537.36'
	    'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:22.0) Gecko/20130328 Firefox/22.0'
	]
	counter = 0
	global br
	br = mechanize.Browser()
	br.set_handle_robots(False)
	br.set_handle_redirect(True)
	br.set_handle_referer(True)
	r = br.open(pageweb)
	br.addheaders = [('User-agent', random.choice(fake_agent))]


	# Recherche du formulaire de connexion
	for form in br.forms():
		if "submit=Log in" in str(form):
			br.select_form(nr=counter)
		counter += 1

	# Connexion avec le login / mdp
	br.form['username'] = identifiant
	br.form['password'] = mot2passe
	html = br.submit().read()

	# Est-ce que l'authentification a réussi?  --> Message Welcome username
	check_state = "faux"
	resultat = html.split('\n')
	regex = re.compile(r'(.*)Welcome(.*)'+identifiant,re.IGNORECASE)
	for ligne in resultat: 
		if regex.match(ligne):
			check_state = "vrai"
			break

	req = br.follow_link(text='My Hosts')
	data_html = req.read()

  # On cherche le nombre d'adresse dyndns disponible
	nb_host = re.search(r'You have <strong>(\w)', data_html)
	if nb_host:
		nb_host = int(re.sub(r'You have <strong>','', nb_host.group(0)))
	else:
		nb_host = 0

	print identifiant, ':', nb_host, 'remaining hosts'

	# On affiche la liste des hosts si nb_host < 2
	if nb_host < 2:
		data_html = re.sub(r'\n','',data_html)
		for m in re.finditer(r'<td><a href="/dns/dyndns/(.*)\.dyndns\.org">.*(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*</td>',data_html):
			tableau = re.sub(r'</table>.*','',m.group())
			tableau = re.sub(r'<tr>','',tableau)
			tableau = re.sub(r'<td>','',tableau)
			tableau = re.sub(r'</tr>','\n',tableau)
			tableau = re.sub(r'<td class="hideid">\d*</td>','',tableau)
			tableau = re.sub(r'</a></td><td class="mobileHide">',' ',tableau)
			tableau = re.sub(r'</td>',' ',tableau)
			tableau = re.sub(r'<a.*">','',tableau)

			print tableau

	br.follow_link(text='Log Out')
	mechanize.CookieJar.clear
	return check_state

for etab in username:
	log2dyndns(page_home,etab,password)
	#result = log2dyndns(page_home,etab,password)
	#if result == "vrai":
	#	print "Mise a jour de", etab, "réussi"
	#else:
	#	print "Mise à jour de", etab, "FAILED"
