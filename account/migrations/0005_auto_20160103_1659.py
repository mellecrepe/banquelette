# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20151227_2135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='bank',
            field=models.CharField(max_length=50, choices=[(None, b''), (b'oney', b'Oney'), (b'boursorama', b'Boursorama'), (b'soge', b'Soci\xc3\xa9t\xc3\xa9 G\xc3\xa9n\xc3\xa9rale'), (b'ingdirect', b'ING Direct'), (b'espece', b'Liquide/Esp\xc3\xa8ce')]),
        ),
        migrations.AlterField(
            model_name='account',
            name='comment',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
