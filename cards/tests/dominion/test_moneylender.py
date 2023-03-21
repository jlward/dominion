from cards.kingdom_cards.dominion import Moneylender
from games.factories import GameFactory
from players.factories import PlayerFactory
from testing import BaseTestCase
from turns.factories import AdHocTurnFactory, TurnFactory


class MoneylenderCardTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Moneylender()

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

    def test_perform_specific_action_no_copper(self):
        self.deck.hand = ['Estate'] * 4
        with self.assert_adhoc_turn_not_created():
            self.card.perform_specific_action(
                deck=self.deck,
                turn=self.turn,
            )


class MoneylenderFormTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Moneylender()
        self.adhoc_turn = AdHocTurnFactory(
            player=self.player,
            game=self.game,
            turn=self.turn,
            card=self.card,
        )

    def test_decline_trashing(self):
        trash = self.game.trash_pile[:]
        hand = self.deck.hand[:]
        money = self.turn.available_money
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, selection='1')
        assert form.is_valid()
        form.save()
        self.deck.refresh_from_db()
        self.game.refresh_from_db()
        self.turn.refresh_from_db()
        self.assertEqual(self.game.trash_pile, trash)
        self.assertEqual(self.deck.hand, hand)
        self.assertEqual(self.turn.available_money, money)

    def test_trash_copper(self):
        trash = self.game.trash_pile[:]
        hand = self.deck.hand[:]
        money = self.turn.available_money
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, selection='0')
        assert form.is_valid()
        form.save()
        self.deck.refresh_from_db()
        self.assertEqual(len(self.game.trash_pile), len(trash) + 1)
        self.assertEqual(len(self.deck.hand), len(hand) - 1)
        self.assertEqual(self.turn.available_money, money + 3)
