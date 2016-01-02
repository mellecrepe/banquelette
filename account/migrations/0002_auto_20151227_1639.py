# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='bank',
            field=models.CharField(max_length=50, choices=[(None, b''), (b'oney', b'Oney'), (b'boursorama', b'Boursorama'), (b'soge', b'Soci\xc3\xa9t\xc3\xa9 G\xc3\xa9n\xc3\xa9rale'), (b'espece', b'Liquide/Esp\xc3\xa8ce')]),
        ),
        migrations.AlterField(
            model_name='account',
            name='category',
            field=models.CharField(max_length=50, choices=[(None, b''), (b'necessaire', b'N\xc3\xa9cessaire'), (b'achat', b'Achat'), (b'sortie', b'Sortie'), (b'vacances', b'Vacances'), (b'gain', b'Gain'), (b'autre', b'Autre')]),
        ),
        migrations.AlterField(
            model_name='account',
            name='comment',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='subcategory',
            field=models.CharField(max_length=50, choices=[(None, b''), (b'courses', b'N\xc3\xa9cessaire/Courses'), (b'transport', b'N\xc3\xa9cessaire/Transport'), (b'electricite', b'N\xc3\xa9cessaire/El\xc3\xa9ctricit\xc3\xa9'), (b'loyer', b'N\xc3\xa9cessaire/Loyer'), (b'repas-midi', b'N\xc3\xa9cessaire/Repas midi'), (b'sante', b'N\xc3\xa9cessaire/Sant\xc3\xa9'), (b'impot-taxe', b'N\xc3\xa9cessaire/Imp\xc3\xb4t - Taxe'), (b'assurance', b'N\xc3\xa9cessaire/Assurance'), (b'telephone-box', b'N\xc3\xa9cessaire/T\xc3\xa9l\xc3\xa9phone - Box'), (b'necessaire-autre', b'N\xc3\xa9cessaire/Autre'), (b'vetement', b'Achat/V\xc3\xaatement'), (b'cadeau', b'Achat/Cadeau'), (b'decoration', b'Achat/D\xc3\xa9coration'), (b'box', b'Achat/Box'), (b'beaute', b'Achat/Beaut\xc3\xa9'), (b'achat-divers', b'Achat/Divers'), (b'resto', b'Sortie/Resto'), (b'bar', b'Sortie/Bar'), (b'gourmandise', b'Sortie/Gourmandise'), (b'soiree', b'Sortie/Soir\xc3\xa9e'), (b'concert', b'Sortie/Concerts'), (b'cine', b'Sortie/Cin\xc3\xa9'), (b'theatre', b'Sortie/Th\xc3\xa9atre'), (b'expo-musee', b'Sortie/Expo - Mus\xc3\xa9e'), (b'sport', b'Sortie/Sport'), (b'sortie-autre', b'Sortie/Autre'), (b'vacances', b'Vacances'), (b'weekend', b'Vacances/Weekend'), (b'paye', b'Gain/Paye'), (b'remboursement', b'Gain/Remboursement'), (b'argent-cadeau', b'Gain/Argent (cadeau)'), (b'gain-autre', b'Gain/Autre'), (b'autre', b'Autre'), (b'retrait', b'Autre/Retrait'), (b'nicolas', b'Autre/Nicolas')]),
        ),
    ]
