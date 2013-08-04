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
usage: dyndns [-h] [-u USER] [-p PASSWORD] [--update] [-d]

Update Dyndns account and retrieve some usefull data.

optional arguments:
  -h, --help   show this help message and exit
  -u USER      dyndns account (required)
  -p PASSWORD  dyndns password (required)
  --update     update only, do not retrieve anything (optionnal)
  -d           use dictionnary, you need to create dyndns.conf file
               (optionnal)
```

## Note

Ce script a été écrit en grande partie par un potes et vue qu'il va mettre 10 ans pour se créer un compte, je host son projet chez moi.
