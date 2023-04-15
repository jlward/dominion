from unittest import mock

from cards.kingdom_cards.dominion import Cellar
from games.factories import GameFactory
from players.factories import PlayerFactory
from testing import BaseTestCase
from turns.factories import AdHocTurnFactory, TurnFactory


class CellarCardTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Cellar()

    def test_perform_specific_action(self):
        with self.assert_stacked_turn_created(2):
            stacked_turns = self.card.perform_specific_action(
                deck=self.deck,
                turn=self.turn,
            )
        stacked_turn = stacked_turns[0]
        self.assert_stacked_turn(
            stacked_turn=stacked_turn,
            turn=self.turn,
            player=self.player,
            game=self.game,
            card=self.card,
        )
        stacked_turn = stacked_turns[1]
        self.assert_stacked_turn(
            stacked_turn=stacked_turn,
            turn=self.turn,
            player=self.player,
            game=self.game,
            card=self.card,
            perform_simple_actions=True,
        )


class CellarFormTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Cellar()
        self.adhoc_turn = AdHocTurnFactory(
            player=self.player,
            game=self.game,
            turn=self.turn,
            card=self.card,
        )

    def test_cards_are_discarded_cards_are_drawn(self):
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, cards=['Copper'])
        assert form.is_valid()
        with mock.patch(
            'decks.models.Deck.discard_cards',
        ) as discard_cards, mock.patch(
            'decks.models.Deck.draw_cards',
        ) as draw_cards:
            form.save()
        discard_cards.assert_called_once()
        draw_cards.assert_called_once_with(1)

    def test_is_valid_false_card_not_in_hand(self):
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, cards=['Witch'])
        assert not form.is_valid()
