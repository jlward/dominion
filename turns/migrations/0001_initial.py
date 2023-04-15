# Generated by Django 4.1.2 on 2023-04-15 19:00

import cards.fields
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
            name='Turn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('turn_number', models.IntegerField()),
                ('is_current_turn', models.BooleanField(db_index=True, default=True)),
                ('state', models.CharField(choices=[('action', 'Action Phase'), ('buy', 'Buy Phase')], default='action', max_length=10)),
                ('available_actions', models.IntegerField(default=1)),
                ('available_buys', models.IntegerField(default=1)),
                ('available_money', models.IntegerField(default=0)),
                ('actions_played', models.JSONField(default=list)),
                ('cards_trashed', models.JSONField(default=list)),
                ('reactions_played', models.JSONField(default=list)),
                ('treasures_played', models.JSONField(default=list)),
                ('buys_used', models.JSONField(default=list)),
                ('cards_bought', models.JSONField(default=list)),
                ('cards_gained', models.JSONField(default=list)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='turns', to='games.game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='turns', to='players.player')),
            ],
            options={
                'index_together': {('game', 'is_current_turn')},
            },
        ),
        migrations.CreateModel(
            name='StackedTurn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_current_turn', models.BooleanField(db_index=True, default=True)),
                ('card', cards.fields.CardField(max_length=100)),
                ('turn_order', models.IntegerField(default=0)),
                ('perform_simple_actions', models.BooleanField(default=False)),
                ('card_form_field_string', models.CharField(default='adhocturn_form', max_length=250)),
                ('card_form_title_field_string', models.CharField(default='adhocturn_action_title', max_length=250)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stacked_turns', to='games.game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stacked_turns', to='players.player')),
                ('target_player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='players.player')),
                ('turn', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='stacked_turns', to='turns.turn')),
            ],
        ),
        migrations.CreateModel(
            name='AdHocTurn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_current_turn', models.BooleanField(db_index=True, default=True)),
                ('card', cards.fields.CardField(max_length=100)),
                ('turn_order', models.IntegerField(default=0)),
                ('card_form_field_string', models.CharField(default='adhocturn_form', max_length=250)),
                ('card_form_title_field_string', models.CharField(default='adhocturn_action_title', max_length=250)),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='adhoc_turns', to='games.game')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='adhoc_turns', to='players.player')),
                ('target_player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='players.player')),
                ('turn', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='adhoc_turns', to='turns.turn')),
            ],
        ),
    ]
