from django.test import TestCase

from cards import Copper, Estate, Silver
from turns.factories import TurnFactory


class TurnPlayTreasuresTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.turn = TurnFactory()

    def assert_monies(self, *, available_money, treasures_played):
        self.turn.refresh_from_db()
        self.assertEqual(self.turn.available_money, available_money)
        self.assertCountEqual(self.turn.treasures_played, treasures_played)

    def test_smoke(self):
        cards = [Copper(), Silver()]
        self.turn.play_treasures(cards)
        self.assert_monies(available_money=3, treasures_played=['Copper', 'Silver'])

    def test_no_money(self):
        cards = []
        self.turn.play_treasures(cards)
        self.assert_monies(available_money=0, treasures_played=[])

    def test_available_nonzero(self):
        cards = [Copper(), Silver()]
        self.turn.available_money = 1
        self.turn.play_treasures(cards)
        self.assert_monies(available_money=4, treasures_played=['Copper', 'Silver'])

    def test_played_not_empty(self):
        cards = [Copper(), Silver()]
        self.turn.treasures_played = ['Foo']
        self.turn.play_treasures(cards)
        self.assert_monies(
            available_money=3,
            treasures_played=['Foo', 'Copper', 'Silver'],
        )

    # TODO remove estate or something
    def test_non_money(self):
        cards = [Copper(), Silver(), Estate()]
        self.turn.play_treasures(cards)
        self.assert_monies(
            available_money=3,
            treasures_played=['Copper', 'Silver', 'Estate'],
        )
