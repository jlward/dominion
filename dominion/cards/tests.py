from django.test import TestCase

import dominion.cards
from dominion.cards.apps import CardAppConfig, create_cards
from dominion.cards.models import Card, CardInstance, Treasure, Victory
from dominion.games.factories import GameFactory


class SmokeTestCase(TestCase):
    def test_string_method(self):
        for card in Card.objects.all():
            self.assertEqual(str(card), card.name.title())


class PostMigrateTestCase(TestCase):
    def test_copper_card_is_in_db(self):
        card = Card.objects.get(name='copper')
        self.assertEqual(card.cost, 0)
        self.assertEqual(card.count, 60)
        self.assertEqual(card.treasure.money_value, 1)

    def test_silver_card_is_in_db(self):
        card = Card.objects.get(name='silver')
        self.assertEqual(card.cost, 3)
        self.assertEqual(card.count, 40)
        self.assertEqual(card.treasure.money_value, 2)

    def test_gold_card_is_in_db(self):
        card = Card.objects.get(name='gold')
        self.assertEqual(card.cost, 6)
        self.assertEqual(card.count, 30)
        self.assertEqual(card.treasure.money_value, 3)

    def test_create_cards_multiple_times_does_not_cause_problems(self):
        sender = CardAppConfig('dominion.cards', dominion.cards)
        sender.models = {
            'treasure': Treasure,
            'victory': Victory,
        }
        create_cards(sender)
        card = Card.objects.get(name='copper')
        self.assertEqual(card.cost, 0)
        self.assertEqual(card.count, 60)
        self.assertEqual(card.treasure.money_value, 1)

    def test_estate_card_is_in_db(self):
        card = Card.objects.get(name='estate')
        self.assertEqual(card.cost, 2)
        self.assertEqual(card.count, 12)
        self.assertEqual(card.victory.points, 1)

    def test_duchy_card_is_in_db(self):
        card = Card.objects.get(name='duchy')
        self.assertEqual(card.cost, 5)
        self.assertEqual(card.count, 12)
        self.assertEqual(card.victory.points, 3)

    def test_province_card_is_in_db(self):
        card = Card.objects.get(name='province')
        self.assertEqual(card.cost, 8)
        self.assertEqual(card.count, 12)
        self.assertEqual(card.victory.points, 6)


class CreateForCardTestCase(TestCase):
    def setUp(self):
        self.game = GameFactory()

    def test_create_coppers(self):
        card = Card.objects.get(name='copper')
        with self.assertNumQueries(1):
            CardInstance.objects.create_for_card(card, self.game)
        self.assertEqual(self.game.cardinstance_set.count(), 60)
