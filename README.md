# Projet LOG2DYNDNS

Ce script permet de se connecter à l'ensemble de vos comptes dyndns.

## Pré-requis
Ce projet utilise le module python mechanize. Sur une Debian, on l'installe de cette manière :
```bash
apt-get install python-mechanize
```

## Paramétrage
Il faut éditer le script et modifier les paramètres ```username``` et ```password``` comme ceci :
```python
username = ['account']
password = 'password'
```

## Utilisation
```bash
./log2dyndns.py
```
