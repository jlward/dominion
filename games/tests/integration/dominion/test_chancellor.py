from ..testcases import IntegrationTestCase


class ChancellorNoDrawPileTestCase(IntegrationTestCase):
    player_starting_hand = ['Chancellor']
    player_starting_draw_pile = []

    def test(self):
        self.play_card(self.player, 'Chancellor')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)


class ChancellorDrawPileTestCase(IntegrationTestCase):
    player_starting_hand = ['Chancellor']
    player_starting_draw_pile = ['Copper']

    def test(self):
        self.play_card(self.player, 'Chancellor')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)
