from ..testcases import IntegrationTestCase


class SpyTestCase(IntegrationTestCase):
    player_starting_hand = ['Spy']
    player_starting_draw_pile = ['Village', 'Estate']
    opponent_starting_draw_pile = ['Gold', 'Village']

    def test(self):
        self.play_card(self.player, 'Spy')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.pick_yes_no_from_modal(self.player, self.SELECTION_NO)

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.pick_yes_no_from_modal(self.player, self.SELECTION_YES)

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)


class SpyNoCardsLeftToDrawTestCase(IntegrationTestCase):
    player_starting_hand = ['Spy']
    player_starting_draw_pile = []
    opponent_starting_draw_pile = []
    opponent_starting_discard_pile = ['Gold']

    def test(self):
        self.play_card(self.player, 'Spy')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.pick_yes_no_from_modal(self.player, self.SELECTION_YES)

        self.assert_adhoc_model_for_player(self.player, False)
