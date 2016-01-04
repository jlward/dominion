# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('players', '0001_initial'),
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Turn',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('turn_number', models.PositiveSmallIntegerField(db_index=True)),
                ('actions_left', models.PositiveSmallIntegerField(default=1)),
                ('buys_left', models.PositiveSmallIntegerField(default=1)),
                ('game', models.ForeignKey(to='games.Game')),
                ('player', models.ForeignKey(to='players.Player')),
            ],
        ),
    ]
