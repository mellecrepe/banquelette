#-*- coding: utf-8 -*-
import datetime
from django import forms
from couchdbkit.ext.django.forms  import DocumentForm
from account.models import Account

CATEGORY_CHOICES = (
    (None, ''),
    ('courses', 'Necessaire/Courses'),
    ('transport', 'Necessaire/Transport'),
    ('electricite', 'Necessaire/Eléctricité'),
    ('loyer', 'Necessaire/Loyer'),
    ('repas-midi', 'Necessaire/Repas midi'),
    ('sante', 'Necessaire/Santé'),
    ('impot-taxe', 'Necessaire/Impôt - Taxe'),
    ('assurance', 'Necessaire/Assurance'),
    ('telephone-box', 'Necessaire/Téléphone - Box'),
    ('necessaire-autre', 'Necessaire/Autre'),
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

BANK_CHOICES = (
    (None, ''),
    ('oney', 'Oney'),
    ('boursorama', 'Boursorama'),
    ('soge', 'Société Générale'),
)

YEAR_CHOICES = (
    ('2015', '2015'),
    ('2016', '2016'),
)

MONTH_CHOICES = (
    ('01', 'Janvier'),
    ('02', 'Février'),
    ('03', 'Mars'),
    ('04', 'Avril'),
    ('05', 'Mai'),
    ('06', 'Juin'),
    ('07', 'Juillet'),
    ('08', 'Aout'),
    ('09', 'Septembre'),
    ('10', 'Octobre'),
    ('11', 'Novembre'),
    ('12', 'Décembre'),
)


class AccountForm(DocumentForm):
    subcategory = forms.CharField(widget=forms.Select(choices=CATEGORY_CHOICES), required=False)
    bank = forms.CharField(required = False, widget=forms.Select(choices=BANK_CHOICES))
    delete = forms.BooleanField(required=False)

    class Meta:
        document = Account

class UpdateDbForm(forms.Form):
    data = forms.CharField(label='Nouvelles données', widget=forms.Textarea)
    bank = forms.ChoiceField(label='Banque', choices=BANK_CHOICES)

class MonthChoiceForm(forms.Form):
    year = forms.ChoiceField(label='Année', choices=YEAR_CHOICES)
    month = forms.ChoiceField(label='Mois', choices=MONTH_CHOICES)
