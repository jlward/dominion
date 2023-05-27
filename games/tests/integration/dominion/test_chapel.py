from ..testcases import IntegrationTestCase


class ChapelWithHandTestCase(IntegrationTestCase):
    player_starting_hand = ['Chapel', 'Silver', 'Gold', 'Smithy']

    def test(self):
        self.play_card(self.player, 'Chapel')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.player_pick_cards_from_modal('Silver', 'Gold')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_resources_for_player(self.player, actions=0, buys=1, money=0)
        self.assert_hand(self.player, ['Smithy'])


class ChapelWithoutHandTestCase(IntegrationTestCase):
    player_starting_hand = ['Chapel']

    def test(self):
        self.play_card(self.player, 'Chapel')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_resources_for_player(self.player, actions=0, buys=1, money=0)
        self.assert_hand(self.player, [])
