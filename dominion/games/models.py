import random

from django.db import models

from jsonfield import JSONField

from dominion.cards.models import Card, CardInstance
from dominion.decks.models import Deck


class Game(models.Model):
    players = models.ManyToManyField('players.Player')
    player_order = JSONField(default=[])

    def add_player(self, player):
        self.players.add(player)
        self.player_order.append(player.pk)
        random.shuffle(self.player_order)
        self.save()

    def create_card_instances(self):
        for card in Card.objects.all():
            CardInstance.objects.create_for_card(card, self)

    def start(self):
        players = list(self.players.all())
        Deck.objects.bulk_create(
            Deck(game=self, player=player)
            for player in players
        )
