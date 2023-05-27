from ..testcases import IntegrationTestCase


class ThiefChoiceTestCase(IntegrationTestCase):
    player_starting_hand = ['Thief']
    opponent_starting_draw_pile = ['Gold', 'Silver']

    def test(self):
        self.play_card(self.player, 'Thief')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.pick_cards_from_modal(self.player, 'Gold')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.pick_cards_from_modal(self.player, 'Gold')
        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)


class ThiefOneTreaureChoiceTestCase(IntegrationTestCase):
    player_starting_hand = ['Thief']
    opponent_starting_draw_pile = ['Gold']

    def test(self):
        self.play_card(self.player, 'Thief')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.pick_cards_from_modal(self.player, 'Gold')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)


class ThiefNoTreaureNoChoiceTestCase(IntegrationTestCase):
    player_starting_hand = ['Thief']
    opponent_starting_draw_pile = ['Estate', 'Duchy']

    def test(self):
        self.play_card(self.player, 'Thief')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)
