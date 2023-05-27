from ..testcases import IntegrationTestCase


class ThroneRoomTestCase(IntegrationTestCase):
    player_starting_hand = ['ThroneRoom', 'ThroneRoom', 'Smithy', 'Feast', 'Feast']
    player_starting_draw_pile = [
        'Village',
        'Silver',
        'Copper',
        'Estate',
        'Feast',
        'Thief',
    ]

    def test_throne_room_smithy(self):
        self.assert_initial_state()

        self.player_play_card('ThroneRoom')

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.player_pick_cards_from_modal('Smithy')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        r = self.player_client.get(self.game_url)
        self.assertEqual(self.get_resources(r), dict(actions=0, buys=1, money=0))
        self.assertCountEqual(
            self.get_player_hand(r),
            [
                'ThroneRoom',
                'Feast',
                'Feast',
                'Village',
                'Silver',
                'Copper',
                'Estate',
                'Feast',
                'Thief',
            ],
        )

    def test_throne_room_feast(self):
        self.assert_initial_state()

        self.player_play_card('ThroneRoom')

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.player_pick_cards_from_modal('Feast')

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        r = self.player_client.get(self.game_url)
        self.assertCountEqual(
            self.get_player_hand(r),
            ['ThroneRoom', 'Smithy', 'Feast'],
        )

        self.player_pick_cards_from_modal('Silver')

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.player_pick_cards_from_modal('Silver')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        r = self.player_client.get(self.game_url)
        self.assertEqual(self.get_resources(r), dict(actions=0, buys=1, money=0))
        self.assertCountEqual(
            self.get_player_hand(r),
            ['ThroneRoom', 'Smithy', 'Feast'],
        )

    def test_throne_room_throne_room_smithy_village(self):
        self.assert_initial_state()

        self.player_play_card('ThroneRoom')

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        self.player_pick_cards_from_modal('ThroneRoom')

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        r = self.player_client.get(self.game_url)
        self.assertCountEqual(self.get_player_hand(r), ['Smithy', 'Feast', 'Feast'])

        self.player_pick_cards_from_modal('Smithy')

        self.assert_player_adhoc_turn_modal_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        r = self.player_client.get(self.game_url)
        self.assertCountEqual(
            self.get_player_hand(r),
            [
                'Feast',
                'Feast',
                'Village',
                'Silver',
                'Copper',
                'Estate',
                'Feast',
                'Thief',
            ],
        )

        self.player_pick_cards_from_modal('Village')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()

        r = self.player_client.get(self.game_url)
        self.assertEqual(self.get_resources(r), dict(actions=4, buys=1, money=0))
        self.assertCountEqual(
            self.get_player_hand(r),
            ['Feast', 'Feast', 'Silver', 'Copper', 'Estate', 'Feast', 'Thief'],
        )


class ThroneRoomNoOtherCardsInHandTestCase(IntegrationTestCase):
    player_starting_hand = ['ThroneRoom']

    def test(self):
        self.assert_initial_state()

        self.player_play_card('ThroneRoom')

        self.assert_player_adhoc_turn_modal_not_present()
        self.assert_opponent_adhoc_turn_modal_not_present()
        r = self.player_client.get(self.game_url)
        self.assertEqual(self.get_resources(r), dict(actions=0, buys=1, money=0))
        self.assertCountEqual(self.get_player_hand(r), [])
