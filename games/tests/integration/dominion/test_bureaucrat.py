from ..testcases import IntegrationTestCase


class BureaucratNoChoiceTestCase(IntegrationTestCase):
    player_starting_hand = ['Bureaucrat']
    opponent_starting_hand = ['Copper', 'Estate']

    def test(self):
        self.play_card(self.player, 'Bureaucrat')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_player_turn(self.player, True)
        self.assert_resources_for_player(self.player, actions=0, buys=1, money=0)
        self.assert_hand(self.opponent, ['Copper'])


class BureaucratNoChoiceNoVicrotryCardTestCase(IntegrationTestCase):
    player_starting_hand = ['Bureaucrat']
    opponent_starting_hand = ['Copper']

    def test(self):
        self.play_card(self.player, 'Bureaucrat')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_player_turn(self.player, True)
        self.assert_resources_for_player(self.player, actions=0, buys=1, money=0)
        self.assert_hand(self.opponent, ['Copper'])


class BureaucratChoiceTestCase(IntegrationTestCase):
    player_starting_hand = ['Bureaucrat']
    opponent_starting_hand = ['Copper', 'Estate', 'Estate']

    def test(self):
        self.play_card(self.player, 'Bureaucrat')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, True)

        self.pick_cards_from_modal(self.opponent, 'Estate')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_player_turn(self.player, True)
        self.assert_resources_for_player(self.player, actions=0, buys=1, money=0)
        self.assert_hand(self.opponent, ['Copper', 'Estate'])
