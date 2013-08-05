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
usage: dyndns [-h] [-u USER] [-p PASSWORD] [--hostname HOSTNAME] [--create]
              [--delete] [--update] [-l] [-c]

Manage your Dyndns Account.

optional arguments:
  -h, --help           show this help message and exit
  -u USER              dyndns account (required)
  -p PASSWORD          dyndns password (required)
  --hostname HOSTNAME  dns domain name of your host (use only with --create,
                       --delete, --update options)
  --create             create a domain name for your host on dyndns
                       (optionnal)
  --delete             delete an existing domain name on your dyndns account
                       (optionnal)
  --update             update ip address of your host on dyndns (optionnal)
  -l, --list           list hosts on your account (optionnal)
  -c, --config         use dictionnary, you need to create dyndns.conf file
                       (optionnal)

```

## Note

Ce script a été écrit en grande partie par un potes et vue qu'il va mettre 10 ans pour se créer un compte, je host son projet chez moi.
