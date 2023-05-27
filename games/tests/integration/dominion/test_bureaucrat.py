from ..testcases import IntegrationTestCase


class BureaucratNoChoiceTestCase(IntegrationTestCase):
    player_starting_hand = ['Bureaucrat']
    opponent_starting_hand = ['Copper', 'Estate']

    def test(self):
        self.player_play_card('Bureaucrat')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        r = self.player_client.get(self.game_url)
        self.assert_player_turn(self.player, True)
        self.assertEqual(self.get_resources(r), dict(actions=0, buys=1, money=0))
        self.assert_hand(self.opponent, ['Copper'])


class BureaucratNoChoiceNoVicrotryCardTestCase(IntegrationTestCase):
    player_starting_hand = ['Bureaucrat']
    opponent_starting_hand = ['Copper']

    def test(self):
        self.player_play_card('Bureaucrat')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        r = self.player_client.get(self.game_url)
        self.assert_player_turn(self.player, True)
        self.assertEqual(self.get_resources(r), dict(actions=0, buys=1, money=0))
        self.assert_hand(self.opponent, ['Copper'])


class BureaucratChoiceTestCase(IntegrationTestCase):
    player_starting_hand = ['Bureaucrat']
    opponent_starting_hand = ['Copper', 'Estate', 'Estate']

    def test(self):
        self.player_play_card('Bureaucrat')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_present()

        self.oppenent_pick_cards_from_modal('Estate')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        r = self.player_client.get(self.game_url)
        self.assert_player_turn(self.player, True)
        self.assertEqual(self.get_resources(r), dict(actions=0, buys=1, money=0))
        self.assert_hand(self.opponent, ['Copper', 'Estate'])
