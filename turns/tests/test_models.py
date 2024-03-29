from unittest import mock

from django.test import TestCase

from cards.base import Card
from cards.kingdom_cards.base_cards import Copper, Estate, Silver
from cards.kingdom_cards.dominion import Smithy, Village
from decks.factories import DeckFactory
from testing import BaseTestCase
from turns.factories import AdHocTurnFactory, TurnFactory


class TurnPlayActionTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.turn = TurnFactory()
        self.deck = DeckFactory(
            game=self.turn.game,
            player=self.turn.player,
            hand=['Village', 'Smithy'],
        )
        self.village = Village()
        self.smithy = Smithy()

    def assert_action_played(self):
        self.deck.refresh_from_db()
        self.turn.refresh_from_db()
        self.assertEqual(self.turn.actions_played, ['Village'])
        self.assertEqual(self.deck.played_cards, ['Village'])
        self.assertEqual(
            self.deck.hand,
            ['Smithy', 'Smithy'],
        )
        self.assertEqual(self.turn.available_actions, 2)

    def test_ghost_action(self):
        with mock.patch('decks.models.Deck.play_card') as play_card:
            self.turn.play_action(self.village, ghost_action=True)
        play_card.assert_not_called()

    def test_not_ghost_action(self):
        with mock.patch('decks.models.Deck.play_card') as play_card:
            self.turn.play_action(self.village, ghost_action=False)
        play_card.assert_called_once_with(self.village)

    def test_consumed(self):
        actions = self.turn.available_actions
        self.turn.play_action(self.smithy, consume=True)
        self.turn.refresh_from_db()
        self.assertEqual(self.turn.available_actions, actions - 1)

    def test_not_consumed(self):
        actions = self.turn.available_actions
        self.turn.play_action(self.smithy, consume=False)
        self.turn.refresh_from_db()
        self.assertEqual(self.turn.available_actions, actions)

    def test_smoke(self):
        with self.assert_stacked_turn_created():
            self.turn.play_action(self.village)


class TurnPlayTreasuresTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.turn = TurnFactory()

    def assert_monies(self, *, available_money, treasures_played):
        self.turn.refresh_from_db()
        self.assertEqual(self.turn.available_money, available_money)
        self.assertCountEqual(self.turn.treasures_played, treasures_played)

    def test_smoke(self):
        cards = [Copper(), Silver()]
        self.turn.play_treasures(cards)
        self.assert_monies(available_money=3, treasures_played=['Copper', 'Silver'])

    def test_no_money(self):
        cards = []
        self.turn.play_treasures(cards)
        self.assert_monies(available_money=0, treasures_played=[])

    def test_available_nonzero(self):
        cards = [Copper(), Silver()]
        self.turn.available_money = 1
        self.turn.play_treasures(cards)
        self.assert_monies(available_money=4, treasures_played=['Copper', 'Silver'])

    def test_played_not_empty(self):
        cards = [Copper(), Silver()]
        self.turn.treasures_played = ['Foo']
        self.turn.play_treasures(cards)
        self.assert_monies(
            available_money=3,
            treasures_played=['Foo', 'Copper', 'Silver'],
        )

    # TODO remove estate or something
    def test_non_money(self):
        cards = [Copper(), Silver(), Estate()]
        self.turn.play_treasures(cards)
        self.assert_monies(
            available_money=3,
            treasures_played=['Copper', 'Silver', 'Estate'],
        )


class TestPerformBuyTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.turn = TurnFactory(available_money=10)
        self.deck = DeckFactory(game=self.turn.game, player=self.turn.player)
        self.village = Village()

    def assert_buying(self):
        self.turn.refresh_from_db()
        self.deck.refresh_from_db()
        self.assertEqual(self.turn.game.kingdom['Village'], 9)
        self.assertIn('Village', self.deck.discard_pile)
        self.assertEqual(self.turn.available_money, 7)
        self.assertEqual(self.turn.available_buys, 0)

    def test_smoke(self):
        self.turn.perform_buy(self.village)
        self.assert_buying()


class TestPerformCleanupTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.turn = TurnFactory()
        self.deck = DeckFactory(
            game=self.turn.game,
            player=self.turn.player,
            discard_pile=[],
            draw_pile=['Copper'] * 6,
            played_cards=['Village'] * 3,
            hand=['Silver'] * 4,
        )

    def assert_cleanup(self):
        self.turn.refresh_from_db()
        self.deck.refresh_from_db()
        assert not self.turn.is_current_turn
        self.assertEqual(len(self.deck.hand), 5)
        self.assertEqual(len(self.deck.played_cards), 0)
        self.assertCountEqual(self.deck.draw_pile, ['Copper'])
        self.assertCountEqual(
            self.deck.discard_pile,
            (['Village'] * 3) + (['Silver'] * 4),
        )
        self.assertCountEqual(self.deck.hand, ['Copper'] * 5)

    def test_smoke(self):
        self.turn.perform_cleanup()
        self.assert_cleanup()


class AdHocTurnCardFieldTestCase(TestCase):
    def test_is_card(self):
        turn = AdHocTurnFactory(card='Smithy')
        turn.refresh_from_db()
        assert isinstance(turn.card, Card)

    def test_save_card_class_get_card(self):
        turn = AdHocTurnFactory(card=Village)
        turn.refresh_from_db()
        assert isinstance(turn.card, Card)

    def test_save_card_object_get_card(self):
        turn = AdHocTurnFactory(card=Village())
        turn.refresh_from_db()
        assert isinstance(turn.card, Card)

    def test_non_card_object_is_not_valid(self):
        class Foo:
            pass

        with self.assertRaises(TypeError):
            AdHocTurnFactory(card=Foo)
