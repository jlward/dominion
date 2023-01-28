# Generated by Django 4.1.2 on 2023-01-28 21:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('players', '0001_initial'),
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Deck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('draw_pile', models.JSONField(default=list)),
                ('discard_pile', models.JSONField(default=list)),
                ('hand', models.JSONField(default=list)),
                ('played_cards', models.JSONField(default=list)),
                ('duration_cards', models.JSONField(default=list)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='decks', to='games.game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='decks', to='players.player')),
            ],
        ),
    ]
