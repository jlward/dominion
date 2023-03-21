from unittest import mock

from cards.kingdom_cards.dominion import Militia
from games.factories import GameFactory
from players.factories import PlayerFactory
from testing import BaseTestCase
from turns.factories import AdHocTurnFactory, TurnFactory


class MilitiaCardTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Militia()

    def test_perform_specific_action(self):
        with self.assert_adhoc_turn_created(len(self.game.players.all()) - 1):
            adhoc_turns = self.card.perform_specific_action(
                deck=self.deck,
                turn=self.turn,
            )
        for player in self.game.players.all():
            if player.pk == self.player.pk:
                continue
            player_turns = [turn for turn in adhoc_turns if turn.player.pk == player.pk]
            self.assertEqual(len(player_turns), 1)
            self.assert_adhoc_turn(
                adhoc_turn=player_turns[0],
                turn=self.turn,
                player=player,
                game=self.game,
                card=self.card,
            )


class MilitiaFormTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.other_players = PlayerFactory.create_batch(11)
        self.target_player = self.other_players[0]
        self.game = GameFactory(players=[self.player] + self.other_players)
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Militia()
        self.adhoc_turn = AdHocTurnFactory(
            player=self.target_player,
            game=self.game,
            turn=self.turn,
            card=self.card,
        )

    def test_hand_full(self):
        deck = self.game.decks.get(player=self.target_player)
        # cards = the cards being kept
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, cards=deck.hand[:3])
        assert form.is_valid()
        with mock.patch('decks.models.Deck.discard_cards') as discard_cards:
            form.save()
        discard_cards.assert_called_once()

    def test_hand_of_three(self):
        deck = self.game.decks.get(player=self.target_player)
        deck.hand = ['Copper'] * 3
        deck.save()
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, cards=deck.hand)
        assert form.is_valid()
        with mock.patch('decks.models.Deck.discard_cards') as discard_cards:
            form.save()
        discard_cards.assert_called_once()

    def test_keep_too_many(self):
        deck = self.game.decks.get(player=self.target_player)
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, cards=deck.hand[:4])
        assert not form.is_valid()

    def test_keep_too_few(self):
        deck = self.game.decks.get(player=self.target_player)
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, cards=deck.hand[:2])
        assert not form.is_valid()

    def test_keep_invalid_cards(self):
        form = (
            self.build_card_form(adhoc_turn=self.adhoc_turn, cards=['Witch', 'Witch']),
        )
        assert not form.is_valid()
