# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0003_victory'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='count',
            field=models.PositiveSmallIntegerField(default=10),
        ),
    ]
