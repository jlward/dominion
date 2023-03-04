from django.test import TestCase
from faker import Faker

from games.models import Game
from players.factories import PlayerFactory


class BaseTestCase(TestCase):
    faker = Faker()

    def create_game(self, kingdom_cards=None):
        if kingdom_cards is None:
            kingdom_cards = ['Village', 'Smithy']
        players = PlayerFactory.create_batch(2)
        game = Game.objects.create_game(players, kingdom_cards)
        game.create_turn(players[0])
        return game
