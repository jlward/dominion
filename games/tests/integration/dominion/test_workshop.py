from ..testcases import IntegrationTestCase


class WorkshopTestCase(IntegrationTestCase):
    player_starting_hand = ['Workshop']

    def test(self):
        self.play_card(self.player, 'Workshop')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.pick_cards_from_modal(self.player, 'Silver')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_resources_for_player(self.player, actions=0, buys=1, money=0)
        self.assert_hand(self.player, [])
