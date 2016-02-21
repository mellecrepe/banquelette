#-*- coding: utf-8 -*-
import datetime
from django import forms
from django.forms import ModelForm
from account.models import Account
from account.settings import *

import categories


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

CATEGORY_CHOICES = [(k, k) for k,cat in categories.FIRST_LEVEL_CATEGORIES.items()]
CATEGORY_CHOICES.insert(0, (None, '------'))

class AccountForm(ModelForm):
    class Meta:
        model = Account
        fields = [ 'date', 'description', 'category', 'expense', 'halve', 'bank', 'check', 'comment']

class UpdateDbForm(forms.Form):
    data = forms.CharField(label='Nouvelles données', widget=forms.Textarea)
    bank = forms.ChoiceField(label='Banque', choices=BANK_CHOICES)

class MonthChoiceForm(forms.Form):
    year = forms.ChoiceField(label='Année', choices=YEAR_CHOICES)
    month = forms.ChoiceField(label='Mois', choices=MONTH_CHOICES)

class SearchForm(forms.Form):
    date_start = forms.DateField(label='Date de début', required=False)
    date_end = forms.DateField(label='Date de fin', required=False)
    category = forms.ChoiceField(label='Catégories', required=False, choices=CATEGORY_CHOICES)
    bank = forms.ChoiceField(label='Banque', required=False, choices=BANK_CHOICES)
    description = forms.CharField(label='Description', required=False)
