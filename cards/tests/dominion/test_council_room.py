from contextlib import contextmanager

from django.test import TestCase

from cards.kingdom_cards.dominion import CouncilRoom
from games.factories import GameFactory
from players.factories import PlayerFactory
from turns.factories import TurnFactory


class CouncilRoomCardTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.other_player = PlayerFactory()
        self.game = GameFactory(players=[self.player, self.other_player])
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.other_deck = self.game.decks.get(player=self.other_player)
        self.card = CouncilRoom()

    @contextmanager
    def assert_council_room(self, deck, num_cards):
        before_draw_pile = deck.draw_pile
        before_hand = deck.hand
        yield
        deck.refresh_from_db()
        after_draw_pile = deck.draw_pile
        after_hand = deck.hand
        self.assertEqual(len(after_hand) - len(before_hand), num_cards)
        self.assertEqual(len(before_draw_pile) - len(after_draw_pile), num_cards)

    def test_perform_specific_action_self(self):
        with self.assert_council_room(self.deck, 0):
            self.card.perform_specific_action(deck=self.deck, turn=self.turn)

    def test_perform_specific_action_other(self):
        with self.assert_council_room(self.other_deck, 1):
            self.card.perform_simple_actions(
                deck=self.other_deck,
                turn=self.turn,
            )
