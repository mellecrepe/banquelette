# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20151227_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='date',
            field=models.DateField(),
        ),
    ]
