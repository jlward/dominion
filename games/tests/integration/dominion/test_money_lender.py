from ..testcases import IntegrationTestCase


class MoneylenderTestCase(IntegrationTestCase):
    player_starting_hand = ['Moneylender', 'Copper']

    def test_trash(self):
        self.player_play_card('Moneylender')

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.player_pick_yes_no_from_modal(self.SELECTION_YES)

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        r = self.player_client.get(self.game_url)
        self.assertEqual(self.get_resources(r), dict(actions=0, buys=1, money=3))
        self.assertCountEqual(self.get_player_hand(r), [])

    def test_do_not_trash(self):
        self.player_play_card('Moneylender')

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.player_pick_yes_no_from_modal(self.SELECTION_NO)

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        r = self.player_client.get(self.game_url)
        self.assertEqual(self.get_resources(r), dict(actions=0, buys=1, money=0))
        self.assertCountEqual(self.get_player_hand(r), ['Copper'])


class MoneylenderNoCopperTestCase(IntegrationTestCase):
    player_starting_hand = ['Moneylender', 'Silver']

    def test(self):
        self.player_play_card('Moneylender')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        r = self.player_client.get(self.game_url)
        self.assertEqual(self.get_resources(r), dict(actions=0, buys=1, money=0))
        self.assertCountEqual(self.get_player_hand(r), ['Silver'])
