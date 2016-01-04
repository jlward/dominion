# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0001_initial'),
        ('games', '0001_initial'),
        ('cards', '0004_card_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='CardInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('card', models.ForeignKey(to='cards.Card')),
                ('deck', models.ForeignKey(blank=True, to='decks.Deck', null=True)),
                ('game', models.ForeignKey(to='games.Game')),
            ],
        ),
    ]
