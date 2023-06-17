from ..testcases import IntegrationTestCase


class WitchTestCase(IntegrationTestCase):
    player_starting_hand = ['Witch']

    def test_provides_actions_and_draws_a_card(self):
        self.play_card(self.player, 'Witch')

        self.assert_player_turn(self.player, True)
        self.assert_hand_size(self.player, 2)
        self.assert_card_in_discard(self.opponent, 'Curse')

        self.assert_player_turn(self.opponent, False)
