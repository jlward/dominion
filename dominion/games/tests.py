import random

from django.test import TestCase

from dominion.games.models import Game
from dominion.players.factories import PlayerFactory


class AddPlayerTestCase(TestCase):
    def setUp(self):
        self.game = Game.objects.create()

    def test_add_player_adds_to_players(self):
        player = PlayerFactory()
        self.game.add_player(player)
        self.assertEqual(
            set(self.game.players.all()),
            set([player]),
        )

    def test_add_player_adds_player_to_player_order(self):
        players = PlayerFactory.create_batch(3)
        for player in players:
            self.game.add_player(player)
        self.assertEqual(
            set(self.game.player_order),
            set(player.pk for player in players),
        )

    def test_player_order_is_random(self):
        random.seed(8)
        player1 = PlayerFactory()
        player2 = PlayerFactory()
        player3 = PlayerFactory()
        player4 = PlayerFactory()

        # Player orders are always random.
        self.game.add_player(player1)
        self.assertEqual(
            self.game.player_order,
            [player1.pk],
        )

        self.game.add_player(player2)
        self.assertEqual(
            self.game.player_order,
            [player2.pk, player1.pk],
        )

        self.game.add_player(player3)
        self.assertEqual(
            self.game.player_order,
            [player1.pk, player2.pk, player3.pk],
        )

        self.game.add_player(player4)
        self.assertEqual(
            self.game.player_order,
            [player2.pk, player4.pk, player1.pk, player3.pk],
        )
