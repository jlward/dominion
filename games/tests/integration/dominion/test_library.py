from ..testcases import IntegrationTestCase


class LibraryLessThanSevenCardsTotalTestCase(IntegrationTestCase):
    player_starting_hand = ['Library']
    player_starting_draw_pile = ['Gold', 'Village', 'Copper']
    player_starting_discard_pile = ['Estate', 'Smithy']

    def test(self):
        self.play_card(self.player, 'Library')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.player_pick_yes_no_from_modal(self.SELECTION_YES)

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.player_pick_yes_no_from_modal(self.SELECTION_NO)

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_resources_for_player(self.player, actions=0, buys=1, money=0)
        self.assert_hand(self.player, ['Gold', 'Village', 'Copper', 'Estate'])


class LibraryMoreThanSevenCardsTotalTestCase(IntegrationTestCase):
    player_starting_hand = ['Library']
    player_starting_draw_pile = ['Gold'] * 10

    def test(self):
        self.play_card(self.player, 'Library')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_resources_for_player(self.player, actions=0, buys=1, money=0)
        self.assert_hand(self.player, ['Gold'] * 7)


class LibraryLastCardPickedMakesSevenTestCase(IntegrationTestCase):
    player_starting_hand = ['Library'] + ['Gold'] * 6
    player_starting_draw_pile = ['Village', 'Gold']

    def test(self):
        self.play_card(self.player, 'Library')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.player_pick_yes_no_from_modal(self.SELECTION_YES)

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_resources_for_player(self.player, actions=0, buys=1, money=0)
        self.assert_hand(self.player, ['Village'] + ['Gold'] * 6)
