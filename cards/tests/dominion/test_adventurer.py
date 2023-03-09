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
    def assert_adventurer(self, deck):
        before_draw_pile = deck.draw_pile.copy()
        before_hand = deck.hand.copy()
        before_discard = deck.discard_pile.copy()
        yield
        deck.refresh_from_db()
        drawn_cards = self.list_diff(before_hand, deck.hand)
        discarded_cards = self.list_diff(before_discard, deck.discard_pile)
        self.assertEqual(len(deck.hand) - len(before_hand), 2)
        self.assertEqual(len(deck.draw_pile), len(before_draw_pile) - 3)
        self.assertEqual(len(deck.discard_pile), len(before_discard) + 1)
        self.assert_cards_type(drawn_cards, 'treasure')
        self.assert_cards_type(discarded_cards, 'treasure', False)

    def test_perform_specific_action_self(self):
        with self.assert_adventurer(self.deck):
            self.card.perform_specific_action(deck=self.deck)
