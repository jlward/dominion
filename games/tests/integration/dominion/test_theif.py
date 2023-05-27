from ..testcases import IntegrationTestCase


class ThiefChoiceTestCase(IntegrationTestCase):
    player_starting_hand = ['Thief']
    opponent_starting_draw_pile = ['Gold', 'Silver']

    def test(self):
        self.play_card(self.player, 'Thief')

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.player_pick_cards_from_modal('Gold')

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.player_pick_cards_from_modal('Gold')
        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()


class ThiefOneTreaureChoiceTestCase(IntegrationTestCase):
    player_starting_hand = ['Thief']
    opponent_starting_draw_pile = ['Gold']

    def test(self):
        self.play_card(self.player, 'Thief')

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.player_pick_cards_from_modal('Gold')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()


class ThiefNoTreaureNoChoiceTestCase(IntegrationTestCase):
    player_starting_hand = ['Thief']
    opponent_starting_draw_pile = ['Estate', 'Duchy']

    def test(self):
        self.play_card(self.player, 'Thief')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()
