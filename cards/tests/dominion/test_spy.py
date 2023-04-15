from unittest import mock

from cards.kingdom_cards.dominion import Spy
from games.factories import GameFactory
from players.factories import PlayerFactory
from testing import BaseTestCase
from turns.factories import AdHocTurnFactory, TurnFactory


class SpyCardTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Spy()

    def test_perform_specific_action(self):
        with self.assert_stacked_turn_created(13):
            stacked_turns = self.card.perform_specific_action(
                deck=self.deck,
                turn=self.turn,
            )
        target_players = []
        for stacked_turn in stacked_turns:
            if stacked_turn.perform_simple_actions:
                continue
            self.assertEqual(stacked_turn.turn, self.turn)
            self.assertEqual(stacked_turn.player, self.player)
            self.assertEqual(stacked_turn.game, self.game)
            self.assertEqual(stacked_turn.card, self.card)

            target_players.append(stacked_turn.target_player)
        self.assertCountEqual(target_players, self.game.players.all())


class SpyFormTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Spy()
        self.adhoc_turn = AdHocTurnFactory(
            player=self.player,
            game=self.game,
            turn=self.turn,
            card=self.card,
            target_player=self.player,
        )

    def test_form_is_valid_selection_is_yes(self):
        form = self.build_card_form(
            adhoc_turn=self.adhoc_turn,
            selection=self.SELECTION_YES,
        )
        assert form.is_valid()
        with mock.patch('decks.models.Deck.draw_cards') as draw_cards:
            form.save()
        draw_cards.assert_called_once_with(1, destination='discard_pile')

    def test_form_is_valid_selection_is_no(self):
        form = self.build_card_form(
            adhoc_turn=self.adhoc_turn,
            selection=self.SELECTION_NO,
        )
        assert form.is_valid()
        with mock.patch('decks.models.Deck.draw_cards') as draw_cards:
            form.save()
        draw_cards.assert_not_called()

    def test_extra_info(self):
        form = self.build_card_form(
            adhoc_turn=self.adhoc_turn,
        )
        expected = f"This is {self.player}'s deck"
        self.assertEqual(form.extra_info(), expected)
