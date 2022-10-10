from django.test import TestCase

from cards import Card


class CardTestCase(TestCase):
    def test_card_buys_returns_zero(self):
        card = Card(name='gold')
        self.assertEqual(card.plus_buys, 0)

    def test_card_actions_returns_zero(self):
        card = Card(name='gold')
        self.assertEqual(card.plus_actions, 0)

    def test_card_cards_returns_zero(self):
        card = Card(name='gold')
        self.assertEqual(card.plus_cards, 0)

    def test_card_treasures_returns_three(self):
        card = Card(name='gold')
        self.assertEqual(card.plus_treasures, 3)

    def test_card_victory_points_returns_three(self):
        card = Card(name='gold')
        self.assertEqual(card.plus_victory_points, 0)

    def test_card_name_does_not_exist(self):
        with self.assertRaises(ValueError):
            Card(name='foobar')
