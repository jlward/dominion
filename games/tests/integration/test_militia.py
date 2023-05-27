from .testcases import IntegrationTestCase


class MilitiaTestCase(IntegrationTestCase):
    player_starting_hand = ['Militia', 'Silver', 'Gold', 'Smithy']
    opponent_starting_hand = ['Copper', 'Estate', 'Copper', 'Estate', 'Village']

    def test_modal_pops_up_when_card_played(self):
        self.assert_initial_state()
        self.player_play_card('Militia')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_present()

        self.oppenent_pick_cards_from_modal('Estate', 'Copper', 'Village')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        r = self.player_client.get(self.game_url)
        self.assert_your_turn(r)
        self.assertEqual(self.get_resources(r), dict(actions=0, buys=1, money=2))
        self.assertCountEqual(self.get_oppnent_hand(r), ['Copper', 'Estate', 'Village'])
