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
        with self.assert_queued_turn_created(1):
            queued_turn = self.card.perform_specific_action(
                deck=self.deck,
                turn=self.turn,
            )
        self.assertEqual(queued_turn.turn, self.turn)
        self.assertEqual(queued_turn.player, self.player)
        self.assertEqual(queued_turn.game, self.game)
        self.assertEqual(queued_turn.card, self.card)


# TODO test form
