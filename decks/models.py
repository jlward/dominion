import operator
import random

from django.db import models

from cards import get_cards_from_names
from cards.fields import CardsField
from decks.managers import DeckManager


class Deck(models.Model):
    objects = DeckManager()
    game = models.ForeignKey(
        'games.Game',
        related_name='decks',
        on_delete=models.PROTECT,
    )
    player = models.ForeignKey(
        'players.Player',
        related_name='decks',
        on_delete=models.PROTECT,
    )

    draw_pile = CardsField()
    discard_pile = CardsField()
    hand = CardsField()
    played_cards = CardsField()
    duration_cards = CardsField()
    narnia_pile = CardsField()

    @property
    def all_cards(self):
        return get_cards_from_names(
            self.draw_pile
            + self.discard_pile
            + self.hand
            + self.duration_cards
            + self.played_cards,
        )

    @property
    def real_draw_pile(self):
        cards = get_cards_from_names(self.draw_pile)
        return sorted(
            cards,
            key=operator.attrgetter('cost', 'name'),
        )

    @property
    def real_discard_pile(self):
        return get_cards_from_names(self.discard_pile)

    @property
    def score(self):
        return sum(card.get_victory_points(self) for card in self.all_cards)

    @property
    def no_actions(self):
        return list(card for card in self.hand if card.is_action) == []

    @property
    def no_treasure(self):
        return list(card for card in self.hand if card.is_treasure) == []

    def top_deck(self):
        if len(self.draw_pile) == 0:
            if len(self.discard_pile) == 0:
                return None
            self.full_shuffle()
        return self.draw_pile.pop(0)

    def draw_cards(self, num, destination='hand'):
        result = []
        for _ in range(num):
            card = self.top_deck()
            if card is None:
                break
            result.append(card)
            getattr(self, destination).append(card)
        return result

    def play_card(self, card):
        self.hand.remove(card.name)
        self.played_cards.append(card.name)

    def discard_cards(self, cards=None):
        if cards is None:
            cards = self.hand

        for card in list(cards):
            self.discard_pile.append(self.hand.pop(self.hand.index(card)))

    def move_to_top_deck(self, card, source='hand'):
        card_source = getattr(self, source)
        card = card_source.pop(card_source.index(card.name))
        self.draw_pile.insert(0, card)

    def move_to_discard(self, card, source='hand'):
        card_source = getattr(self, source)
        card = card_source.pop(card_source.index(card.name))
        self.discard_pile.insert(0, card)

    def cleanup(self):
        self.discard_cards()

        for _ in range(len(self.played_cards)):
            self.discard_pile.append(self.played_cards.pop())

    def full_shuffle(self):
        for _ in range(len(self.discard_pile)):
            self.draw_pile.append(self.discard_pile.pop())
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.draw_pile)

    # Assuming player can only trash from hand
    def trash_cards(self, cards, source='hand'):
        if source not in ['hand', 'played_cards']:
            raise ValueError('invalid source')  # pragma: no cover
        card_source = getattr(self, source)
        for card in cards:
            self.game.trash_pile.append(card.name)
            card_source.pop(card_source.index(card.name))
        self.save()
        self.game.save()
