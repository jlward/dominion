from ..testcases import IntegrationTestCase


class MoatTestCase(IntegrationTestCase):
    player_starting_hand = ['Village', 'Militia']
    opponent_starting_hand = ['Moat', 'Copper', 'Silver', 'Gold']

    def test_not_attacking(self):
        self.play_card(self.player, 'Village')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)

    def test_attacking(self):
        self.play_card(self.player, 'Militia')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, True)

        self.pick_yes_no_from_modal(self.opponent, self.SELECTION_YES)

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)
