# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='money_value',
        ),
        migrations.AddField(
            model_name='treasure',
            name='money_value',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=False,
        ),
    ]
