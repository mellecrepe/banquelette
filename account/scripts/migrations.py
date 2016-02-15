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

categories = [
    { 'old_category' : 'necessaire', 
      'old_subcategory' : 'courses',
      'new_category' : 'Nécessaire/Courses' },
    { 'old_category' : 'necessaire',
      'old_subcategory' : 'transport',
      'new_category' : 'Nécessaire/Transport' },
    { 'old_category' : 'necessaire',
      'old_subcategory' : 'electricite',
      'new_category' : 'Nécessaire/Electricité' },
    { 'old_category' : 'necessaire',
      'old_subcategory' : 'loyer',
      'new_category' : 'Nécessaire/Loyer' },
    { 'old_category' : 'necessaire',
      'old_subcategory' : 'repas-midi',
      'new_category' : 'Nécessaire/Repas midi' },
    { 'old_category' : 'necessaire',
      'old_subcategory' : 'sante',
      'new_category' : 'Nécessaire/Santé' },
    { 'old_category' : 'necessaire',
      'old_subcategory' : 'impot-taxe',
      'new_category' : 'Nécessaire/Impôts et taxes' },
    { 'old_category' : 'necessaire',
      'old_subcategory' : 'assurance',
      'new_category' : 'Nécessaire/Assurance' },
    { 'old_category' : 'necessaire',
      'old_subcategory' : 'telephone-box',
      'new_category' : 'Nécessaire/Téléphone et Internet' },
    { 'old_category' : 'necessaire',
      'old_subcategory' : 'necessaire-autre',
      'new_category' : 'Nécessaire' },
    { 'old_category' : 'achat',
      'old_subcategory' : 'vetement',
      'new_category' : 'Achat/Vêtement' },
    { 'old_category' : 'achat',
      'old_subcategory' : 'cadeau',
      'new_category' : 'Achat/Cadeaux' },
    { 'old_category' : 'achat',
      'old_subcategory' : 'decoration',
      'new_category' : 'Achat/Décoration' },
    { 'old_category' : 'achat',
      'old_subcategory' : 'box',
      'new_category' : 'Achat/Box' },
    { 'old_category' : 'achat',
      'old_subcategory' : 'beaute',
      'new_category' : 'Achat/Beauté' },
    { 'old_category' : 'achat',
      'old_subcategory' : 'achat-divers',
      'new_category' : 'Achat' },
    { 'old_category' : 'sortie',
      'old_subcategory' : 'resto',
      'new_category' : 'Sortie/Restaurant' },
    { 'old_category' : 'sortie',
      'old_subcategory' : 'bar',
      'new_category' : 'Sortie/Bar' },
    { 'old_category' : 'sortie',
      'old_subcategory' : 'gourmandise',
      'new_category' : 'Sortie/Gourmandise' },
    { 'old_category' : 'sortie',
      'old_subcategory' : 'soiree',
      'new_category' : 'Sortie/Soirée' },
    { 'old_category' : 'sortie',
      'old_subcategory' : 'concert',
      'new_category' : 'Sortie/Concert' },
    { 'old_category' : 'sortie',
      'old_subcategory' : 'cine',
      'new_category' : 'Sortie/Cinéma' },
    { 'old_category' : 'sortie',
      'old_subcategory' : 'theatre',
      'new_category' : 'Sortie/Théatre' },
    { 'old_category' : 'sortie',
      'old_subcategory' : 'expo-musee',
      'new_category' : 'Sortie/Expo et Musée' },
    { 'old_category' : 'sortie',
      'old_subcategory' : 'sport',
      'new_category' : 'Sortie/Sport' },
    { 'old_category' : 'sortie',
      'old_subcategory' : 'sortie-autre',
      'new_category' : 'Sortie' },
    { 'old_category' : 'vacances',
      'old_subcategory' : 'vacances',
      'new_category' : 'Vacances' },
    { 'old_category' : 'vacances',
      'old_subcategory' : 'weekend',
      'new_category' : 'Vacances/Weekend' },
    { 'old_category' : 'gain',
      'old_subcategory' : 'paye',
      'new_category' : 'Gain/Paye' },
    { 'old_category' : 'gain',
      'old_subcategory' : 'remboursement',
      'new_category' : 'Gain/Remboursement' },
    { 'old_category' : 'gain',
      'old_subcategory' : 'argent-cadeau',
      'new_category' : 'Gain/Cadeau' },
    { 'old_category' : 'gain',
      'old_subcategory' : 'gain-autre',
      'new_category' : 'Gain'},
    { 'old_category' : 'autre',
      'old_subcategory' : 'autre',
      'new_category' : 'Autre' },
    { 'old_category' : 'autre',
      'old_subcategory' : 'retrait', 
      'new_category' : 'Autre/Retrait'},
    { 'old_category' : 'autre',
      'old_subcategory' : 'nicolas', 
      'new_category' : 'Autre/Nicolas'}
]


# connexion a la base sqlite
conn = sqlite3.connect(sqlite_file)
conn.text_factory = str
cursor = conn.cursor()

for c in categories:
	cursor.execute("""
        	UPDATE account_account SET category=:new_category WHERE category=:old_category AND subcategory=:old_subcategory""", c)

conn.commit()
conn.close()

