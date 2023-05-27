from ..testcases import IntegrationTestCase


class MoneylenderTestCase(IntegrationTestCase):
    player_starting_hand = ['Moneylender', 'Copper']

    def test_trash(self):
        self.play_card(self.player, 'Moneylender')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.pick_yes_no_from_modal(self.player, self.SELECTION_YES)

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_resources_for_player(self.player, actions=0, buys=1, money=3)
        self.assert_hand(self.player, [])

    def test_do_not_trash(self):
        self.play_card(self.player, 'Moneylender')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.pick_yes_no_from_modal(self.player, self.SELECTION_NO)

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_resources_for_player(self.player, actions=0, buys=1, money=0)
        self.assert_hand(self.player, ['Copper'])


class MoneylenderNoCopperTestCase(IntegrationTestCase):
    player_starting_hand = ['Moneylender', 'Silver']

    def test(self):
        self.play_card(self.player, 'Moneylender')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_resources_for_player(self.player, actions=0, buys=1, money=0)
        self.assert_hand(self.player, ['Silver'])
