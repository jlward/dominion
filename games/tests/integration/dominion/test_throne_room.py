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
        self.play_card(self.player, 'ThroneRoom')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.player_pick_cards_from_modal('Smithy')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_resources_for_player(self.player, actions=0, buys=1, money=0)
        self.assert_hand(
            self.player,
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
        self.play_card(self.player, 'ThroneRoom')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.player_pick_cards_from_modal('Feast')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_hand(
            self.player,
            ['ThroneRoom', 'Smithy', 'Feast'],
        )

        self.player_pick_cards_from_modal('Silver')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.player_pick_cards_from_modal('Silver')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_resources_for_player(self.player, actions=0, buys=1, money=0)
        self.assert_hand(
            self.player,
            ['ThroneRoom', 'Smithy', 'Feast'],
        )

    def test_throne_room_throne_room_smithy_village(self):
        self.play_card(self.player, 'ThroneRoom')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.player_pick_cards_from_modal('ThroneRoom')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_hand(self.player, ['Smithy', 'Feast', 'Feast'])

        self.player_pick_cards_from_modal('Smithy')

        self.assert_adhoc_model_for_player(self.player, True)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_hand(
            self.player,
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

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)

        self.assert_resources_for_player(self.player, actions=4, buys=1, money=0)
        self.assert_hand(
            self.player,
            ['Feast', 'Feast', 'Silver', 'Copper', 'Estate', 'Feast', 'Thief'],
        )


class ThroneRoomNoOtherCardsInHandTestCase(IntegrationTestCase):
    player_starting_hand = ['ThroneRoom']

    def test(self):
        self.play_card(self.player, 'ThroneRoom')

        self.assert_adhoc_model_for_player(self.player, False)
        self.assert_adhoc_model_for_player(self.opponent, False)
        self.assert_resources_for_player(self.player, actions=0, buys=1, money=0)
        self.assert_hand(self.player, [])
