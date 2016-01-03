# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20151227_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='check',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='account',
            name='halve',
            field=models.BooleanField(default=False),
        ),
    ]
