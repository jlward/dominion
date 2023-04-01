from unittest import mock

from cards.kingdom_cards.dominion import ThroneRoom
from games.factories import GameFactory
from players.factories import PlayerFactory
from testing import BaseTestCase
from turns.factories import AdHocTurnFactory, TurnFactory


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


class ThroneRoomFormTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = ThroneRoom()
        self.adhoc_turn = AdHocTurnFactory(
            player=self.player,
            game=self.game,
            turn=self.turn,
            card=self.card,
        )

    def test_play_action_called_twice_when_calling_save(self):
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, cards=['Village'])
        assert form.is_valid()
        with mock.patch('turns.models.Turn.play_action') as play_action:
            form.save()
        self.assertEqual(play_action.call_count, 2)
        play_action.assert_has_calls(
            [
                mock.call(mock.ANY, consume=False),
                mock.call(mock.ANY, consume=False, ghost_action=True),
            ],
        )
