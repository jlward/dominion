from ..testcases import IntegrationTestCase


class VillageTestCase(IntegrationTestCase):
    player_starting_hand = ['Village']
    player_starting_draw_pile = ['Gold', 'Smithy']

    def test_provides_actions_and_draws_a_card(self):
        self.player_play_card('Village')

        self.assert_player_turn(self.player, True)
        self.assert_resources_for_player(self.player, actions=2, buys=1, money=0)
        self.assert_hand(self.player, ['Gold'])

        self.assert_player_turn(self.opponent, False)
