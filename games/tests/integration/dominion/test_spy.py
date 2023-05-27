from ..testcases import IntegrationTestCase


class SpyTestCase(IntegrationTestCase):
    player_starting_hand = ['Spy']
    player_starting_draw_pile = ['Village', 'Estate']
    opponent_starting_draw_pile = ['Gold', 'Village']

    def test(self):
        self.play_card(self.player, 'Spy')

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.player_pick_yes_no_from_modal(self.SELECTION_NO)

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.player_pick_yes_no_from_modal(self.SELECTION_YES)

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()


class SpyNoCardsLeftToDrawTestCase(IntegrationTestCase):
    player_starting_hand = ['Spy']
    player_starting_draw_pile = []
    opponent_starting_draw_pile = []
    opponent_starting_discard_pile = ['Gold']

    def test(self):
        self.play_card(self.player, 'Spy')

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.player_pick_yes_no_from_modal(self.SELECTION_YES)

        self.assert_player_adhoc_turn_modal_not_present()
