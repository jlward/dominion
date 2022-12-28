from django.test import TestCase

from decks.factories import DeckFactory


class DeckTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.deck = DeckFactory()

    def test_draw_cards_smoke(self):
        self.deck.draw_cards(1)
        self.assertEqual(len(self.deck.hand), 6)
        self.assertEqual(len(self.deck.draw_pile), 2)
        self.assertEqual(len(self.deck.discard_pile), 2)

    def test_draw_all_cards_from_pile(self):
        self.deck.draw_cards(len(self.deck.draw_pile))
        self.assertEqual(len(self.deck.hand), 8)
        self.assertEqual(len(self.deck.draw_pile), 0)
        self.assertEqual(len(self.deck.discard_pile), 2)

    def test_draw_pile_plus_one(self):
        self.deck.draw_cards(len(self.deck.draw_pile) + 1)
        self.assertEqual(len(self.deck.hand), 9)
        self.assertEqual(len(self.deck.draw_pile), 1)
        self.assertEqual(len(self.deck.discard_pile), 0)

    def test_draw_more_than_all(self):
        self.deck.draw_cards(100)
        self.assertEqual(len(self.deck.hand), 10)
        self.assertEqual(len(self.deck.draw_pile), 0)
        self.assertEqual(len(self.deck.discard_pile), 0)
