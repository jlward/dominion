import uuid

from django.db import models

from games.managers import GameManager


class Game(models.Model):
    objects = GameManager()

    players = models.ManyToManyField('players.Player')
    kingdom = models.JSONField(default=list)
    trash_pile = models.JSONField(default=list)
    game_hash = models.UUIDField()
    turn_order = models.JSONField(default=list)

    def save(self, *args, **kwargs):
        self.game_hash = uuid.uuid4()
        return super().save(*args, **kwargs)
