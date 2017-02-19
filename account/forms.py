#-*- coding: utf-8 -*-
import datetime
from django import forms
from account.models import Account
from account.settings import *

from account.categories import *


YEAR_CHOICES = (
    ('2015', '2015'),
    ('2016', '2016'),
    ('2017', '2017'),
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


BANK_MAJ = BANK_CHOICES[:]
BANK_MAJ.remove(('Argent Liquide', 'Argent Liquide'))
BANK_MAJ.extend([('Boobank/Boursorama', 'Boobank/Boursorama'),
                ('Boobank/Societe Generale', 'Boobank/Societe Generale')])
BANK_MAJ = sorted(BANK_MAJ, key=lambda x: x[1])

CATEGORY_CHOICES = [(k, k) for k,cat in FIRST_LEVEL_CATEGORIES.items()]
CATEGORY_CHOICES.insert(0, (None, '------'))

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('date', 'description', 'category', 'expense', 'halve', 'bank', 'check', 'comment')

class UpdateDbForm(forms.Form):
    data = forms.CharField(label='Nouvelles données', widget=forms.Textarea)
    bank = forms.ChoiceField(label='Banque', choices=BANK_MAJ)

class MonthChoiceForm(forms.Form):
    year = forms.ChoiceField(label='Année', choices=YEAR_CHOICES)
    month = forms.ChoiceField(label='Mois', choices=MONTH_CHOICES)

class SearchForm(forms.Form):
    date_start = forms.DateField(label='De', required=False, widget=forms.TextInput(attrs={'class': 'date'}))
    date_end = forms.DateField(label='A', required=False, widget=forms.TextInput(attrs={'class': 'date'}))
    category = forms.ChoiceField(label='Catégories', required=False, choices=CATEGORY_CHOICES)
    bank = forms.ChoiceField(label='Banque', required=False, choices=BANK_CHOICES)
    description = forms.CharField(label='Description', required=False)
