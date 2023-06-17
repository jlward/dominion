from cards.kingdom_cards.dominion import Library
from games.factories import GameFactory
from players.factories import PlayerFactory
from testing import BaseTestCase
from turns.factories import TurnFactory


class LibraryCardTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Library()

    def test_perform_specific_action(self):
        with self.assert_stacked_turn_created(1):
            stacked_turn = self.card.create_stacked_turns(
                deck=self.deck,
                turn=self.turn,
            )
        self.assertEqual(stacked_turn.turn, self.turn)
        self.assertEqual(stacked_turn.player, self.player)
        self.assertEqual(stacked_turn.game, self.game)
        self.assertEqual(stacked_turn.card, self.card)
