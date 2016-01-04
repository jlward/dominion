# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('decks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deck',
            name='current_hand',
            field=jsonfield.fields.JSONField(default=[]),
        ),
        migrations.AddField(
            model_name='deck',
            name='deck_order',
            field=jsonfield.fields.JSONField(default=[]),
        ),
    ]
