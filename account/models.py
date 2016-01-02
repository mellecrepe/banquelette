#-*- coding: utf-8 -*-
from django.db import models
from account.settings import *

CATEGORY_CHOICES = (
    (None, ''),
    ('necessaire','Nécessaire'),
    ('achat','Achat'),
    ('sortie','Sortie'),
    ('vacances','Vacances'),
    ('gain','Gain'),
    ('autre','Autre'),
)

SUBCATEGORY_CHOICES = (
    (None, ''),
    ('courses', 'Nécessaire/Courses'),
    ('transport', 'Nécessaire/Transport'),
    ('electricite', 'Nécessaire/Eléctricité'),
    ('loyer', 'Nécessaire/Loyer'),
    ('repas-midi', 'Nécessaire/Repas midi'),
    ('sante', 'Nécessaire/Santé'),
    ('impot-taxe', 'Nécessaire/Impôt - Taxe'),
    ('assurance', 'Nécessaire/Assurance'),
    ('telephone-box', 'Nécessaire/Téléphone - Box'),
    ('necessaire-autre', 'Nécessaire/Autre'),
    ('vetement', 'Achat/Vêtement'),
    ('cadeau', 'Achat/Cadeau'),
    ('decoration', 'Achat/Décoration'),
    ('box', 'Achat/Box'),
    ('beaute', 'Achat/Beauté'),
    ('achat-divers', 'Achat/Divers'),
    ('resto', 'Sortie/Resto'),
    ('bar', 'Sortie/Bar'),
    ('gourmandise', 'Sortie/Gourmandise'),
    ('soiree', 'Sortie/Soirée'),
    ('concert', 'Sortie/Concerts'),
    ('cine', 'Sortie/Ciné'),
    ('theatre', 'Sortie/Théatre'),
    ('expo-musee', 'Sortie/Expo - Musée'),
    ('sport', 'Sortie/Sport'),
    ('sortie-autre', 'Sortie/Autre'),
    ('vacances', 'Vacances'),
    ('weekend', 'Vacances/Weekend'),
    ('paye', 'Gain/Paye'),
    ('remboursement', 'Gain/Remboursement'),
    ('argent-cadeau', 'Gain/Argent (cadeau)'),
    ('gain-autre', 'Gain/Autre'),
    ('autre', 'Autre'),
    ('retrait', 'Autre/Retrait'),
    ('nicolas', 'Autre/Nicolas'),
)

class Account(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=150)
    expense = models.FloatField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=50, choices=SUBCATEGORY_CHOICES)
    bank = models.CharField(max_length=50, choices=BANK_CHOICES)
    check = models.BooleanField(default=False)
    halve = models.BooleanField(default=False)
    comment = models.CharField(max_length=200, blank=True)
    
    def save(self, *args, **kwargs):
        necessaire = ['necessaire','courses', 'transport', 'electricite', 'loyer', 'repas-midi', 'sante', 'impot-taxe', 'assurance', 'telephone-box', 'necessaire-autre']
        achat = ['achat', 'vetement', 'cadeau', 'decoration', 'box', 'beaute', 'achat-divers']
        sortie = ['sortie', 'resto', 'bar', 'gourmandise', 'soiree', 'concert', 'cine', 'theatre', 'expo-musee', 'sport', 'sortie-autre']
        vacances = ['vacances', 'weekend']
        gain = ['gain', 'paye', 'remboursement', 'argent-cadeau', 'gain-autre']
        autre = ['autre', 'retrait', 'nicolas']
        
        for list in [ necessaire, achat, sortie, vacances, gain, autre ]:
            if self.subcategory in list:
                self.category = list[0]
        
        super(Account, self).save(*args, **kwargs)
