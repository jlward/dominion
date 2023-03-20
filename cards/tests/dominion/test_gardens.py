from django.test import TestCase

from cards.kingdom_cards.dominion import Gardens
from games.factories import GameFactory
from players.factories import PlayerFactory
from turns.factories import TurnFactory


class GardensCardTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Gardens()

    def test_victory_points_small_deck(self):
        self.deck.hand.pop()
        self.assertEqual(self.card.get_victory_points(self.deck), 0)

    def test_victory_points_med_deck(self):
        self.deck.draw_pile.extend(['Copper'] * 22)
        self.assertEqual(self.card.get_victory_points(self.deck), 3)

    def test_victory_points_large_deck(self):
        self.deck.draw_pile.extend(['Village'] * 90)
        self.assertEqual(self.card.get_victory_points(self.deck), 10)
