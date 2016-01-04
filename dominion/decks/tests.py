import random

from django.test import TestCase

from dominion.decks.models import Deck
from dominion.games.factories import GameFactory
from dominion.players.factories import PlayerFactory


class DeckTestCase(TestCase):
    def setUp(self):
        random.seed(0)

        self.game = GameFactory()
        self.player = PlayerFactory()
        self.game.add_player(self.player)
        self.game.start()

        self.deck = Deck.objects.get(
            game=self.game,
            player=self.player,
        )

    def test_current_hand_is_five(self):
        self.assertEqual(len(self.deck.current_hand), 5)
        self.assertEqual(len(self.deck.deck_order), 5)

    def test_cards_are_cached_on_the_deck(self):
        with self.assertNumQueries(1):
            self.assertEqual(len(self.deck.cards), 10)
        with self.assertNumQueries(0):
            self.assertEqual(len(self.deck.cards), 10)
