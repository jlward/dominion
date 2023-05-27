from ..testcases import IntegrationTestCase


class MilitiaTestCase(IntegrationTestCase):
    player_starting_hand = ['Militia', 'Silver', 'Gold', 'Smithy']
    opponent_starting_hand = ['Copper', 'Estate', 'Copper', 'Estate', 'Village']

    def test(self):
        self.play_card(self.player, 'Militia')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_present()

        self.oppenent_pick_cards_from_modal('Estate', 'Copper', 'Village')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.assert_player_turn(self.player, True)
        self.assert_resources_for_player(self.player, actions=0, buys=1, money=2)
        self.assert_hand(self.opponent, ['Copper', 'Estate', 'Village'])


class MilitiaOpponentShortCardsTestCase(IntegrationTestCase):
    player_starting_hand = ['Militia', 'Silver', 'Gold', 'Smithy']
    opponent_starting_hand = ['Copper', 'Estate', 'Village']

    def test(self):
        self.play_card(self.player, 'Militia')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()
