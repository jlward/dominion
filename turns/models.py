from django.db import models

from turns.managers import TurnManager


class Turn(models.Model):
    objects = TurnManager()

    player = models.ForeignKey(
        'players.Player',
        related_name='turns',
        on_delete=models.PROTECT,
    )
    game = models.ForeignKey(
        'games.Game',
        related_name='turns',
        on_delete=models.PROTECT,
    )
    turn_number = models.IntegerField()
    is_current_turn = models.BooleanField(default=True, db_index=True)
    # Standard card stuff
    available_actions = models.IntegerField(default=1)
    available_buys = models.IntegerField(default=1)
    available_money = models.IntegerField(default=0)

    # What cards were played
    actions_played = models.JSONField(default=list)
    # What cards were trashed
    cards_trashed = models.JSONField(default=list)
    # Who played what reaction card
    reactions_played = models.JSONField(default=list)
    # End of turn stuff
    treasures_played = models.JSONField(default=list)
    buys_used = models.JSONField(default=list)
    cards_bought = models.JSONField(default=list)
    cards_gained = models.JSONField(default=list)

    class Meta:
        index_together = [
            ('game', 'is_current_turn'),
        ]
