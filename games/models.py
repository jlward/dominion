import uuid

from django.db import models


class Game(models.Model):
    players = models.ManyToManyField('players.Player')
    kingdom = models.JSONField(default=list)
    game_hash = models.UUIDField()

    def save(self, *args, **kwargs):
        self.game_hash = uuid.uuid4()
        return super().save(*args, **kwargs)
