#-*- coding: utf-8 -*-

from account import settings

# dictionnaire pour modifier le descriptif
# cle : description originale
# valeur : nouvelle description
auto_description = {
    settings.old_desc_salary: settings.new_desc_salary,
    settings.old_desc_rent: settings.new_desc_rent,
    'SOJIDIS': 'CARREFOUR CITY',
    'PICARD SA 0055': 'PICARD',
    'PICARD SA 094': 'PICARD',
    'AUTEUIL MARKET': 'G20',
    'A2PAS': 'Auchan',
    '1195MARKS SPENC': 'MARKS SPENCER',
    'COJEAN BEAUGRENELL5': 'COJEAN',
    'H & M 208': 'H & M',
    'ETAM P.A.P': 'ETAM',
    'REDOUTE AUB VAD - ROUBAIX': 'La Redoute',
    'DECATHLON 0090': 'DECATHLON',
    'A 4 PATTES': 'Rivolux',
    'REST.KEVIK': 'Bagelstein',
}

# dictionnaire pour organiser les subcategory
# automatiquement
# cle: description (originale)
# valeur: subcategory
auto_subcategory = {
    settings.new_desc_salary: 'paye',
    settings.new_desc_rent: 'loyer',
    'E D F': 'electricite',
    'MONOP': 'courses',
    'CARREFOUR': 'courses',
    'AUTEUIL MARKET': 'courses',
    'G20': 'courses',
    'AUCHAN': 'courses',
    'INTERMARCHE': 'courses',
    'PICARD': 'courses',
    'CARREFOUR CITY': 'courses',
    'Auchan': 'courses',
    'MARKS SPENCER': 'repas-midi',
    'COJEAN': 'repas-midi',
    'QUINDICI': 'repas-midi',
    'SNCF': 'transport',
    'La Redoute': 'vetement',
    'ETAM': 'vetement',
    'H & M': 'vetement',
    'ZARA': 'vetement',
    'STRADIVARIUS': 'vetement',
    'DECATHLON': 'sport',
    'MY LITTLE PARIS': 'box',
    'GAMBETTES BOX': 'box',
    'ARCHI BAR': 'bar',
    'DERNIER METRO': 'bar',
    'LE SEMAPHORE': 'bar',
    'BAR': 'bar',
    'bar': 'bar',
    'MC DONALDS': 'resto',
    'CASTORAMA': 'decoration', 
    'RETRAIT DAB': 'retrait',
    'retrait': 'retrait',
}

