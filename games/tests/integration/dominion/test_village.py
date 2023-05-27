from ..testcases import IntegrationTestCase


class VillageTestCase(IntegrationTestCase):
    player_starting_hand = ['Village']

    def test_provides_actions_and_draws_a_card(self):
        self.player_play_card('Village')

        r = self.player_client.get(self.game_url)
        self.assert_your_turn(r)
        self.assertEqual(self.get_resources(r), dict(actions=2, buys=1, money=0))
        self.assertEqual(len(self.get_player_hand(r)), 1)

        r = self.opponent_client.get(self.game_url)
        self.assert_not_your_turn(r)
