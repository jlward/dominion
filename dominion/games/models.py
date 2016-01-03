import random

from django.db import models

from jsonfield import JSONField


class Game(models.Model):
    players = models.ManyToManyField('players.Player')
    player_order = JSONField(default=[])

    def add_player(self, player):
        self.players.add(player)
        self.player_order.append(player.pk)
        random.shuffle(self.player_order)
        self.save()
