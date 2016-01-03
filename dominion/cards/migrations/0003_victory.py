# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0002_auto_20160103_1940'),
    ]

    operations = [
        migrations.CreateModel(
            name='Victory',
            fields=[
                ('card_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cards.Card')),
                ('points', models.PositiveSmallIntegerField()),
            ],
            bases=('cards.card',),
        ),
    ]
