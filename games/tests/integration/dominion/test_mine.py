from ..testcases import IntegrationTestCase


class MineTestCase(IntegrationTestCase):
    player_starting_hand = ['Mine', 'Copper', 'Silver', 'Gold']

    def test_say_yes(self):
        self.player_play_card('Mine')

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.player_pick_cards_from_modal('Copper', kingdom_card='Silver')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        r = self.player_client.get(self.game_url)
        self.assertEqual(self.get_resources(r), dict(actions=0, buys=1, money=0))
        self.assertCountEqual(self.get_player_hand(r), ['Silver', 'Gold'])


class MineNoTreasureTestCase(IntegrationTestCase):
    player_starting_hand = ['Mine', 'Village']

    def test_say_yes(self):
        self.player_play_card('Mine')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        r = self.player_client.get(self.game_url)
        self.assertEqual(self.get_resources(r), dict(actions=0, buys=1, money=0))
        self.assertCountEqual(self.get_player_hand(r), ['Village'])
