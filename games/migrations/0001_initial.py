# Generated by Django 4.1.2 on 2022-10-10 21:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('players', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                (
                    'id',
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('kingdom', models.JSONField(default=list)),
                ('game_hash', models.UUIDField()),
                ('players', models.ManyToManyField(to='players.player')),
            ],
        ),
    ]
