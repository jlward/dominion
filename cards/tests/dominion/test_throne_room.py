# from unittest import mock

from cards.kingdom_cards.dominion import ThroneRoom
from games.factories import GameFactory
from players.factories import PlayerFactory
from testing import BaseTestCase
from turns.factories import TurnFactory


class ThroneRoomCardTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = ThroneRoom()

    def test_perform_specific_action(self):
        with self.assert_adhoc_turn_created():
            adhoc_turn = self.card.perform_specific_action(
                deck=self.deck,
                turn=self.turn,
            )
        self.assert_adhoc_turn(
            adhoc_turn=adhoc_turn,
            turn=self.turn,
            player=self.player,
            game=self.game,
            card=self.card,
        )
