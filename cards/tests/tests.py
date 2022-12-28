import os

from django.conf import settings
from django.test import TestCase

import cards
from cards.base import Card
from cards.kingdom_cards.base_cards import Gold


class CardTestCase(TestCase):
    def test_card_name_returns_gold(self):
        card = Gold()
        self.assertEqual(card.name, 'Gold')

    def test_card_buys_returns_zero(self):
        card = Gold()
        self.assertEqual(card.plus_buys, 0)

    def test_card_actions_returns_zero(self):
        card = Gold()
        self.assertEqual(card.plus_actions, 0)

    def test_card_cards_returns_zero(self):
        card = Gold()
        self.assertEqual(card.plus_cards, 0)

    def test_card_treasures_returns_three(self):
        card = Gold()
        self.assertEqual(card.plus_treasures, 3)

    def test_card_victory_points_returns_three(self):
        card = Gold()
        self.assertEqual(card.plus_victory_points, 0)

    def test_card_cost_returns_six(self):
        card = Gold()
        self.assertEqual(card.cost, 6)


class SmokeTestCase(TestCase):
    def get_cards(self):
        all_cards = cards.get_all_cards()
        for card in all_cards.values():
            yield card

    def test_all_cards_have_a_cost(self):
        failures = []
        for CardClass in self.get_cards():
            card = CardClass()
            try:
                card.cost
            except Exception:
                failures.append(card.name)
        if failures:
            message = '\n'.join(f'{name} is missing a cost' for name in failures)
            message = f'\n{message}'
            raise AssertionError(message)

    def test_all_cards_have_a_type(self):
        failures = []
        for CardClass in self.get_cards():
            card = CardClass()
            try:
                types = card.types
            except Exception:
                failures.append(card.name)
            assert isinstance(types, list)
        if failures:
            message = '\n'.join(f'{name} is missing a type' for name in failures)
            message = f'\n{message}'
            raise AssertionError(message)

    def test_base_card_types(self):
        with self.assertRaises(NotImplementedError):
            Card().types
