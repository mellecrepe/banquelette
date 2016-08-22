#!/usr/bin/python
#-*- coding: utf-8 -*-

# Ce script permet de modifier la base sqlite afin d'utiliser
# la nouvelle gestion de categories
#
# La liste categories peut être adapté au besoin
# Ce script doit être exécuté avant de passer à la version 2.1


from couchdbkit import *
import sqlite3

sqlite_file = 'db.sqlite3.account'

banks = [
    { 'old_bank' : 'oney',
      'new_bank' : 'Oney' },
    { 'old_bank' : 'boursorama',
      'new_bank' : 'Boursorama' },
    { 'old_bank' : 'soge',
      'new_bank' : 'Société Générale' },
    { 'old_bank' : 'ingdirect',
      'new_bank' : 'ING Direct' },
    { 'old_bank' : 'banquepopulaire',
      'new_bank' : 'Banque Populaire' },
    { 'old_bank' : 'espece',
      'new_bank' : 'Argent Liquide' },
]


# connexion a la base sqlite
conn = sqlite3.connect(sqlite_file)
conn.text_factory = str
cursor = conn.cursor()

for b in banks:
    print "Migration de " + b["old_bank"]
    cursor.execute("""
        UPDATE account_account SET bank=:new_bank WHERE bank=:old_bank""", b)

conn.commit()
conn.close()

