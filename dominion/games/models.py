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

    @property
    def get_players(self):
        if hasattr(self, '_get_players'):
            return self._get_players
        self._get_players = {
            player.pk: player
            for player in self.players.all()
        }
        return self._get_players

    @property
    def current_player(self):
        try:
            current_turn = Turn.objects.filter(game=self).latest('turn_number')
        except Turn.DoesNotExist:
            return self.get_players[self.player_order[0]]
        return current_turn.player

    def start(self):
        self.create_card_instances()
        players = self.get_players.values()
        for player in players:
            deck = Deck.objects.create(game=self, player=player)
            deck.get_starting_cards()
        Turn.objects.create(
            player=self.current_player,
            game=self,
            turn_number=1,
        )


class Turn(models.Model):
    player = models.ForeignKey('players.Player')
    game = models.ForeignKey('games.Game')
    turn_number = models.PositiveSmallIntegerField(db_index=True)

    actions_left = models.PositiveSmallIntegerField(default=1)
    buys_left = models.PositiveSmallIntegerField(default=1)
