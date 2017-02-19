# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20160216_2231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='bank',
            field=models.CharField(max_length=50, choices=[(None, b'------'), (b'Argent Liquide', b'Argent Liquide'), (b'Banque Populaire', b'Banque Populaire'), (b'Boursorama', b'Boursorama'), (b'ING Direct', b'ING Direct'), (b'Oney', b'Oney'), (b'Societe Generale', b'Soci\xc3\xa9t\xc3\xa9 G\xc3\xa9n\xc3\xa9rale')]),
        ),
        migrations.AlterField(
            model_name='account',
            name='category',
            field=models.CharField(max_length=50, choices=[('Achats', 'Achats'), ('Achats/Beaut\xe9', 'Achats/Beaut\xe9'), ('Achats/Box', 'Achats/Box'), ('Achats/Cadeaux', 'Achats/Cadeaux'), ('Achats/D\xe9coration', 'Achats/D\xe9coration'), ('Achats/V\xeatements', 'Achats/V\xeatements'), ('Autre', 'Autre'), ('Autre/Nicolas', 'Autre/Nicolas'), ('Autre/Retrait', 'Autre/Retrait'), ('Gain', 'Gain'), ('Gain/Cadeau', 'Gain/Cadeau'), ('Gain/Paye', 'Gain/Paye'), ('Gain/Remboursement', 'Gain/Remboursement'), ('Non-class\xe9', 'Non-class\xe9'), ('N\xe9cessaire', 'N\xe9cessaire'), ('N\xe9cessaire/Assurance', 'N\xe9cessaire/Assurance'), ('N\xe9cessaire/Courses', 'N\xe9cessaire/Courses'), ('N\xe9cessaire/Imp\xf4ts et taxes', 'N\xe9cessaire/Imp\xf4ts et taxes'), ('N\xe9cessaire/Loyer', 'N\xe9cessaire/Loyer'), ('N\xe9cessaire/Repas de midi', 'N\xe9cessaire/Repas de midi'), ('N\xe9cessaire/Sant\xe9', 'N\xe9cessaire/Sant\xe9'), ('N\xe9cessaire/Transport', 'N\xe9cessaire/Transport'), ('N\xe9cessaire/T\xe9l\xe9phone et Internet', 'N\xe9cessaire/T\xe9l\xe9phone et Internet'), ('N\xe9cessaire/\xc9lectricit\xe9', 'N\xe9cessaire/\xc9lectricit\xe9'), ('Sorties', 'Sorties'), ('Sorties/Bar', 'Sorties/Bar'), ('Sorties/Cin\xe9ma', 'Sorties/Cin\xe9ma'), ('Sorties/Concert', 'Sorties/Concert'), ('Sorties/Expo et Mus\xe9e', 'Sorties/Expo et Mus\xe9e'), ('Sorties/Gourmandise', 'Sorties/Gourmandise'), ('Sorties/Restaurant', 'Sorties/Restaurant'), ('Sorties/Soir\xe9e', 'Sorties/Soir\xe9e'), ('Sorties/Sport', 'Sorties/Sport'), ('Sorties/Th\xe9\xe2tre', 'Sorties/Th\xe9\xe2tre'), ('Vacances', 'Vacances'), ('Vacances/Week-end', 'Vacances/Week-end')]),
        ),
    ]
