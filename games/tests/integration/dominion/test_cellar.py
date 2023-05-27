from ..testcases import IntegrationTestCase


class CellarNoCardsTestCase(IntegrationTestCase):
    player_starting_hand = ['Cellar']

    def test(self):
        self.play_card(self.player, 'Cellar')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_player_turn(self.player, True)
        self.assert_resources_for_player(self.player, actions=1, buys=1, money=0)


class CellarCardsInHandTestCase(IntegrationTestCase):
    player_starting_hand = ['Cellar', 'Copper']
    player_starting_draw_pile = ['Gold', 'Estate']

    def test(self):
        self.play_card(self.player, 'Cellar')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.player_pick_cards_from_modal('Copper')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_player_turn(self.player, True)
        self.assert_resources_for_player(self.player, actions=1, buys=1, money=0)

        self.assert_hand(self.player, ['Gold'])
