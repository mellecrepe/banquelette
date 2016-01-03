# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('description', models.CharField(max_length=150)),
                ('expense', models.FloatField()),
                ('category', models.CharField(max_length=50)),
                ('subcategory', models.CharField(max_length=50)),
                ('bank', models.CharField(max_length=50)),
                ('check', models.BooleanField()),
                ('halve', models.BooleanField()),
                ('comment', models.CharField(max_length=200)),
            ],
        ),
    ]
