from ..testcases import IntegrationTestCase


class RemodelTestCase(IntegrationTestCase):
    player_starting_hand = ['Remodel', 'Estate']

    def test(self):
        self.play_card(self.player, 'Remodel')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.player_pick_cards_from_modal('Estate', kingdom_card='Silver')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)


class RemodelNoCardInHandTestCase(IntegrationTestCase):
    player_starting_hand = ['Remodel']

    def test(self):
        self.play_card(self.player, 'Remodel')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)
