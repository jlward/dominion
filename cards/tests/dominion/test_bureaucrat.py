from unittest import mock

from cards.kingdom_cards.dominion import Bureaucrat
from games.factories import GameFactory
from players.factories import PlayerFactory
from testing import BaseTestCase
from turns.factories import AdHocTurnFactory, TurnFactory


class BureaucratCardTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.other_players = PlayerFactory.create_batch(11)
        self.game = GameFactory(players=[self.player] + self.other_players)
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Bureaucrat()

    def test_perform_specific_action_two_victory_cards(self):
        for player in self.other_players:
            deck = self.game.decks.get(player=player)
            deck.hand = ['Copper', 'Estate', 'Estate', 'Village']
            deck.save()

        with self.assert_stacked_turn_created(12):
            self.card.perform_specific_action(
                deck=self.deck,
                turn=self.turn,
            )

    def test_perform_specific_action_one_victory_card(self):
        for player in self.other_players:
            deck = self.game.decks.get(player=player)
            deck.hand = ['Copper', 'Estate', 'Chapel', 'Village']
            deck.save()

        with self.assert_stacked_turn_created(12):
            self.card.perform_specific_action(
                deck=self.deck,
                turn=self.turn,
            )

    def test_perform_specific_action_no_victory_cards(self):
        for player in self.other_players:
            deck = self.game.decks.get(player=player)
            deck.hand = ['Copper', 'Gold', 'Chapel', 'Village']
            deck.save()

        with self.assert_stacked_turn_created(12):
            self.card.perform_specific_action(
                deck=self.deck,
                turn=self.turn,
            )


class BureaucratFormTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Bureaucrat()
        self.adhoc_turn = AdHocTurnFactory(
            player=self.player,
            game=self.game,
            turn=self.turn,
            card=self.card,
        )

    def test_cards_are_moved(self):
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, cards=['Estate'])
        assert form.is_valid()
        with mock.patch('decks.models.Deck.move_to_top_deck') as moved:
            form.save()
        # self.assert_called_once_with(card=mock.ANY) not working
        moved.assert_called_once()

    def test_more_than_max_not_valid(self):
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, cards=self.deck.hand)
        assert not form.is_valid()

    def test_is_valid_false_card_not_in_hand(self):
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, cards=['Witch'])
        assert not form.is_valid()
