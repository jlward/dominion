from unittest import mock

from cards.kingdom_cards.dominion import Feast
from games.factories import GameFactory
from players.factories import PlayerFactory
from testing import BaseTestCase
from turns.factories import AdHocTurnFactory, TurnFactory


class FeastCardTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Feast()

    def test_perform_specific_action(self):
        self.deck.played_cards.append('Feast')
        with self.assert_adhoc_turn_created():
            adhoc_turn = self.card.perform_specific_action(
                deck=self.deck,
                turn=self.turn,
            )
        assert 'Feast' not in self.deck.played_cards
        assert 'Feast' in self.game.trash_pile
        self.assert_adhoc_turn(
            adhoc_turn=adhoc_turn,
            turn=self.turn,
            player=self.player,
            game=self.game,
            card=self.card,
        )


class FeastFormTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Feast()
        self.adhoc_turn = AdHocTurnFactory(
            player=self.player,
            game=self.game,
            turn=self.turn,
            card=self.card,
        )

    def test_card_gained(self):
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, cards=['Copper'])
        assert form.is_valid()
        with mock.patch('games.models.Game.gain_card') as gain_card:
            form.save()
        gain_card.assert_called_once_with(
            self.deck,
            mock.ANY,
        )

    def test_is_valid_false_card_not_in_kingdom(self):
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, cards=['Witch'])
        assert not form.is_valid()
