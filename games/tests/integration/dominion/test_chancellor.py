from ..testcases import IntegrationTestCase


class ChancellorNoDrawPileTestCase(IntegrationTestCase):
    player_starting_hand = ['Chancellor']
    player_starting_draw_pile = []

    def test(self):
        self.assert_initial_state()

        self.player_play_card('Chancellor')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()


class ChancellorDrawPileTestCase(IntegrationTestCase):
    player_starting_hand = ['Chancellor']
    player_starting_draw_pile = ['Copper']

    def test(self):
        self.assert_initial_state()

        self.player_play_card('Chancellor')

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()
