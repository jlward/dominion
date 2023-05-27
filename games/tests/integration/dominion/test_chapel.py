from ..testcases import IntegrationTestCase


class ChapelWithHandTestCase(IntegrationTestCase):
    player_starting_hand = ['Chapel', 'Silver', 'Gold', 'Smithy']

    def test(self):
        self.player_play_card('Chapel')

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.player_pick_cards_from_modal('Silver', 'Gold')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        r = self.player_client.get(self.game_url)
        self.assertEqual(self.get_resources(r), dict(actions=0, buys=1, money=0))
        self.assertCountEqual(self.get_player_hand(r), ['Smithy'])


class ChapelWithoutHandTestCase(IntegrationTestCase):
    player_starting_hand = ['Chapel']

    def test(self):
        self.player_play_card('Chapel')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        r = self.player_client.get(self.game_url)
        self.assertEqual(self.get_resources(r), dict(actions=0, buys=1, money=0))
        self.assertCountEqual(self.get_player_hand(r), [])
