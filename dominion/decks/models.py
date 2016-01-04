from django.db import models


class Deck(models.Model):
    game = models.ForeignKey('games.Game')
    player = models.ForeignKey('players.Player')
