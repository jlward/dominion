from ..testcases import IntegrationTestCase


class RemodelTestCase(IntegrationTestCase):
    player_starting_hand = ['Remodel', 'Estate']

    def test(self):
        self.assert_initial_state()

        self.player_play_card('Remodel')

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.player_pick_cards_from_modal('Estate', kingdom_card='Silver')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()


class RemodelNoCardInHandTestCase(IntegrationTestCase):
    player_starting_hand = ['Remodel']

    def test(self):
        self.assert_initial_state()

        self.player_play_card('Remodel')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()
