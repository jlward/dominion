from ..testcases import IntegrationTestCase


class MineTestCase(IntegrationTestCase):
    player_starting_hand = ['Mine', 'Copper', 'Silver', 'Gold']

    def test_say_yes(self):
        self.play_card(self.player, 'Mine')

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.player_pick_cards_from_modal('Copper', kingdom_card='Silver')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.assert_resources_for_player(self.player, actions=0, buys=1, money=0)
        self.assert_hand(self.player, ['Silver', 'Gold'])


class MineNoTreasureTestCase(IntegrationTestCase):
    player_starting_hand = ['Mine', 'Village']

    def test_say_yes(self):
        self.play_card(self.player, 'Mine')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.assert_resources_for_player(self.player, actions=0, buys=1, money=0)
        self.assert_hand(self.player, ['Village'])
