# Dyndns

Ce script permet de gérer l'ensemble de vos comptes dyndns.

## Pré-requis
Ce projet utilise le module python mechanize. Sur une Debian, on l'installe de cette manière :
```bash
apt-get install python-mechanize
apt-get install python-beautifulsoup
```

## Paramétrage
La configuration se fait dans le fichier dyndns.cfg et dans le fichier dyndns.conf pour les comptes.

## Utilisation

Les options disponibles :
```bash
$ ./dyndns
usage: dyndns.py [-h] [--all] [--debug] {connect,list,update} ...

Manage your Dyndns Account.

positional arguments:
  {connect,list,update}
                        sub-command help
    connect             connect hostnames
    list                listing hostnames
    update              update hostnames

optional arguments:
  -h, --help            show this help message and exit
  --all                 Options for all account
  --debug               Debug mode

```
Pour tester la validité d'un login/mot de passe :
```bash
./dyndns --all connect
./dyndns connect -u USER -p PASSWORD
```
Pour lister les différentes machines d'un compte (ou de tout vos comptes):
```bash
./dyndns --all list
./dyndns list -u USER -p PASSWORD
```
Pour mettre à jour un nom d'hôte :
```bash
./dyndns update -u USER -p PASSWORD -H example.dyndns.org
```

