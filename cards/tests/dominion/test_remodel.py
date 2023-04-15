from unittest import mock

from cards.kingdom_cards.dominion import Remodel
from games.factories import GameFactory
from players.factories import PlayerFactory
from testing import BaseTestCase
from turns.factories import AdHocTurnFactory, TurnFactory


class RemodelCardTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Remodel()

    def test_perform_specific_action(self):
        with self.assert_stacked_turn_created():
            stacked_turn = self.card.perform_specific_action(
                deck=self.deck,
                turn=self.turn,
            )
        self.assert_stacked_turn(
            stacked_turn=stacked_turn,
            turn=self.turn,
            player=self.player,
            game=self.game,
            card=self.card,
        )


class RemodelFormTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Remodel()
        self.adhoc_turn = AdHocTurnFactory(
            player=self.player,
            game=self.game,
            turn=self.turn,
            card=self.card,
        )

    def test_card_trashed_card_gained(self):
        form = self.build_card_form(
            adhoc_turn=self.adhoc_turn,
            cards=['Copper'],
            kingdom_card='Estate',
        )
        assert form.is_valid()
        with mock.patch('games.models.Game.trash_cards') as trash_cards, mock.patch(
            'games.models.Game.gain_card',
        ) as gain_card:
            form.save()
        trash_cards.assert_called_once_with(
            deck=self.deck,
            turn=self.turn,
            cards=mock.ANY,
        )
        gain_card.assert_called_once_with(
            self.deck,
            mock.ANY,
        )

    def test_card_not_in_hand(self):
        form = self.build_card_form(
            adhoc_turn=self.adhoc_turn,
            cards=['Gold'],
            kingdom_card='Estate',
        )
        assert not form.is_valid()

    def test_card_not_in_kingdom(self):
        form = self.build_card_form(
            adhoc_turn=self.adhoc_turn,
            cards=['Copper'],
            kingdom_card='Pearl Diver',
        )
        assert not form.is_valid()

    def test_card_too_expensive(self):
        form = self.build_card_form(
            adhoc_turn=self.adhoc_turn,
            cards=['Copper'],
            kingdom_card='Province',
        )
        assert not form.is_valid()

    def test_more_than_max_selected(self):
        form = self.build_card_form(
            adhoc_turn=self.adhoc_turn,
            cards=['Copper'] * 2,
            kingdom_card='Estate',
        )
        assert not form.is_valid()
