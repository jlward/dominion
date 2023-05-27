from ..testcases import IntegrationTestCase


class CellarNoCardsTestCase(IntegrationTestCase):
    player_starting_hand = ['Cellar']

    def test(self):
        self.player_play_card('Cellar')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        r = self.player_client.get(self.game_url)
        self.assert_player_turn(self.player, True)
        self.assertEqual(self.get_resources(r), dict(actions=1, buys=1, money=0))


class CellarCardsInHandTestCase(IntegrationTestCase):
    player_starting_hand = ['Cellar', 'Copper']
    player_starting_draw_pile = ['Gold', 'Estate']

    def test(self):
        self.player_play_card('Cellar')

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.player_pick_cards_from_modal('Copper')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        r = self.player_client.get(self.game_url)
        self.assert_player_turn(self.player, True)
        self.assertEqual(self.get_resources(r), dict(actions=1, buys=1, money=0))

        self.assert_hand(self.player, ['Gold'])
