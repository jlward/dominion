from ..testcases import IntegrationTestCase


class WorkshopTestCase(IntegrationTestCase):
    player_starting_hand = ['Workshop']

    def test(self):
        self.player_play_card('Workshop')

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.player_pick_cards_from_modal('Silver')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.assert_resources_for_player(self.player, actions=0, buys=1, money=0)
        self.assert_hand(self.player, [])
