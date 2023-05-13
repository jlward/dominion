from unittest import mock

from cards.kingdom_cards.dominion import Workshop
from games.factories import GameFactory
from players.factories import PlayerFactory
from testing import BaseTestCase
from turns.factories import AdHocTurnFactory, TurnFactory


class WorkshopCardTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Workshop()

    def test_perform_specific_action(self):
        with self.assert_stacked_turn_created():
            stacked_turn = self.card.create_stacked_turns(
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


class WorkshopFormTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Workshop()
        self.adhoc_turn = AdHocTurnFactory(
            player=self.player,
            game=self.game,
            turn=self.turn,
            card=self.card,
        )

    def test_gain_card_called_when_calling_save(self):
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, cards=['Village'])
        assert form.is_valid()
        with mock.patch('games.models.Game.gain_card') as gain_card:
            form.save()
        gain_card.assert_called_once_with(
            self.deck,
            mock.ANY,
        )

    def test_form_is_invalid_if_kingdom_card_does_not_exist(self):
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, cards=['Spy'])
        assert not form.is_valid()

    def test_form_is_invalid_if_kingdom_card_is_too_expensive(self):
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, cards=['Province'])
        assert not form.is_valid()
