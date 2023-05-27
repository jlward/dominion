from ..testcases import IntegrationTestCase


class MineTestCase(IntegrationTestCase):
    player_starting_hand = ['Mine', 'Copper', 'Silver', 'Gold']

    def test_say_yes(self):
        self.play_card(self.player, 'Mine')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.pick_cards_from_modal(self.player, 'Copper', kingdom_card='Silver')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_resources_for_player(self.player, actions=0, buys=1, money=0)
        self.assert_hand(self.player, ['Silver', 'Gold'])


class MineNoTreasureTestCase(IntegrationTestCase):
    player_starting_hand = ['Mine', 'Village']

    def test_say_yes(self):
        self.play_card(self.player, 'Mine')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_resources_for_player(self.player, actions=0, buys=1, money=0)
        self.assert_hand(self.player, ['Village'])
