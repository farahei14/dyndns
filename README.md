# Projet LOG2DYNDNS

Ce script permet de se connecter à l'ensemble de vos comptes dyndns.

## Pré-requis
Ce projet utilise le module python mechanize. Sur une Debian, on l'installe de cette manière :
```bash
apt-get install python-mechanize
apt-get install python-beautifulsoup
```

## Paramétrage
La configuration se fait dans le fichier dyndns.conf. Le format du fichier est décrit à l'intérieure.

## Utilisation
```bash
$ ./dyndns
usage: dyndns [-h] [-u USER] [-p PASSWORD] [-H HOSTNAME] [-C] [-D] [-U] [-L]
              [-F] [--local_mail LOCALMAIL] [--remote_mail REMOTEMAIL]

Manage your Dyndns Account.

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  dyndns account (required)
  -p PASSWORD, --password PASSWORD
                        dyndns password (required)
  -H HOSTNAME, --hostname HOSTNAME
                        dns domain name of your host (use only with --create,
                        --delete, --update options)
  -C, --create          create a domain name for your host on dyndns
                        (optionnal)
  -D, --delete          delete an existing domain name on your dyndns account
                        (optionnal)
  -U, --update          update ip address of your host on dyndns (optionnal)
  -L, --list            list hosts on your account (optionnal)
  -F, --file            use dictionnary, you need to create dyndns.conf file
                        (optionnal)
  --local_mail LOCALMAIL
                        mail adress local
  --remote_mail REMOTEMAIL
                        mail adress remote
```

## Note

Ce script a été écrit en grande partie par un potes et vue qu'il va mettre 10 ans pour se créer un compte, je host son projet chez moi.
