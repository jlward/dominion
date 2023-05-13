from unittest import mock

from cards.kingdom_cards.dominion import Chapel
from games.factories import GameFactory
from players.factories import PlayerFactory
from testing import BaseTestCase
from turns.factories import AdHocTurnFactory, TurnFactory


class ChapelCardTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Chapel()

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


class ChapelFormTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Chapel()
        self.adhoc_turn = AdHocTurnFactory(
            player=self.player,
            game=self.game,
            turn=self.turn,
            card=self.card,
        )

    def test_cards_are_trashed(self):
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, cards=['Copper'])
        assert form.is_valid()
        with mock.patch('games.models.Game.trash_cards') as trash_cards:
            form.save()
        trash_cards.assert_called_once_with(
            deck=self.deck,
            turn=self.turn,
            cards=mock.ANY,
        )

    def test_more_than_max_not_valid(self):
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, cards=self.deck.hand)
        assert not form.is_valid()

    def test_is_valid_false_card_not_in_hand(self):
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, cards=['Witch'])
        assert not form.is_valid()
