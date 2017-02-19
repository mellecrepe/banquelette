#-*- coding: utf-8 -*-
from django.db import models
from account.settings import *

from account.categories import *

CATEGORY_CHOICES = [ (c,c) for c in CATEGORIES ]
CATEGORY_CHOICES.sort()

BANK_CHOICES = sorted(BANK_CHOICES, key=lambda x: x[1])

class Account(models.Model):
    date = models.DateField()
    description = models.CharField(max_length=150)
    expense = models.FloatField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    bank = models.CharField(max_length=50, choices=BANK_CHOICES)
    check = models.BooleanField(default=False)
    halve = models.BooleanField(default=False)
    comment = models.CharField(max_length=200, blank=True)
