import os

from django.conf import settings
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

    def test_card_cost_returns_six(self):
        card = Card(name='gold')
        self.assertEqual(card.cost, 6)

    def test_card_name_does_not_exist(self):
        with self.assertRaises(ValueError):
            Card(name='foobar')


class SmokeTestCase(TestCase):
    def test_all_cards_have_a_cost(self):
        path = os.path.join(
            settings.BASE_DIR,
            'cards',
            'card_repo',
        )
        failures = []
        for root, dirs, files in os.walk(path):
            if not files:
                continue

            card_name = os.path.split(root)[-1]
            if card_name == '__pycache__':
                continue
            if 'cost.py' not in files:
                failures.append(card_name)
        if failures:
            message = '\n'.join(f'{name} is missing a cost' for name in failures)
            message = f'\n{message}'
            raise AssertionError(message)
