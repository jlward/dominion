from django.test import TestCase

from dominion.cards.apps import create_cards
from dominion.cards.models import Card


class PostMigrateTestCase(TestCase):
    def test_copper_card_is_in_db(self):
        card = Card.objects.get(name='copper')
        self.assertEqual(card.cost, 0)
        self.assertEqual(card.money_value, 1)

    def test_create_cards_multiple_times_does_not_cause_problems(self):
        create_cards(None)
        card = Card.objects.get(name='copper')
        self.assertEqual(card.cost, 0)
        self.assertEqual(card.money_value, 1)
