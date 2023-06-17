from unittest import mock

from ..testcases import IntegrationTestCase


class MoatTestCase(IntegrationTestCase):
    player_starting_hand = ['Bureaucrat', 'Militia', 'Spy', 'Thief', 'Witch', 'Village']
    opponent_starting_hand = ['Moat', 'Estate', 'Duchy', 'Gold']

    def test_not_attacking(self):
        self.play_card(self.player, 'Village')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)

    def test_not_reveal(self):
        self.play_card(self.player, 'Bureaucrat')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, True)

        with mock.patch('cards.base.Card.create_adhoc_turn') as func:
            self.pick_yes_no_from_modal(self.opponent, self.SELECTION_NO)
        func.assert_called_once()

    def test_bureaucrat(self):
        self.play_card(self.player, 'Bureaucrat')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, True)

        with mock.patch('cards.base.Card.create_adhoc_turn') as func:
            self.pick_yes_no_from_modal(self.opponent, self.SELECTION_YES)
        func.assert_not_called()

    def test_militia(self):
        self.play_card(self.player, 'Militia')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, True)

        with mock.patch('cards.base.Card.create_adhoc_turn') as func:
            self.pick_yes_no_from_modal(self.opponent, self.SELECTION_YES)
        func.assert_not_called()

    def test_spy(self):
        self.play_card(self.player, 'Spy')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, True)

        with mock.patch('cards.base.Card.create_adhoc_turn') as func:
            self.pick_yes_no_from_modal(self.opponent, self.SELECTION_YES)
        # creates adhoc turn for self.player not self.opponent
        func.assert_called_once()

    def test_thief(self):
        self.play_card(self.player, 'Thief')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, True)

        with mock.patch('cards.base.Card.create_adhoc_turn') as func:
            self.pick_yes_no_from_modal(self.opponent, self.SELECTION_YES)
        # creates adhoc turn for self.player not self.opponent
        func.assert_called_once()

    def test_witch(self):
        self.play_card(self.player, 'Witch')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, True)

        with mock.patch('cards.base.Card.create_adhoc_turn') as func:
            self.pick_yes_no_from_modal(self.opponent, self.SELECTION_YES)
        func.assert_not_called()
