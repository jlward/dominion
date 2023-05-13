from contextlib import contextmanager

from cards.kingdom_cards.dominion import Adventurer
from games.factories import GameFactory
from players.factories import PlayerFactory
from testing import BaseTestCase
from turns.factories import TurnFactory


class AdventurerCardTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Adventurer()

    @contextmanager
    def assert_adventurer(self, deck, expected_draw=2):
        before_hand = deck.hand[:]
        before_discard = deck.discard_pile[:]
        yield
        deck.refresh_from_db()
        drawn_cards = self.list_diff(before_hand, deck.hand)
        discarded_cards = self.list_diff(before_discard, deck.discard_pile)
        self.assertEqual(len(drawn_cards), expected_draw)
        self.assert_cards_type(drawn_cards, 'treasure')
        self.assert_cards_type(discarded_cards, 'treasure', False)

    def test_perform_specific_action(self):
        with self.assert_adventurer(self.deck):
            self.card.perform_simple_actions(deck=self.deck, turn=self.turn)

    def test_perform_specific_action_empty_draw_pile(self):
        self.deck.draw_pile = []
        with self.assert_adventurer(self.deck, 1):
            self.card.perform_simple_actions(deck=self.deck, turn=self.turn)
