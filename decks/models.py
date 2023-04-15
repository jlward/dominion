import random

from django.db import models

from cards import get_cards_from_names
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

    draw_pile = models.JSONField(default=list)
    discard_pile = models.JSONField(default=list)
    hand = models.JSONField(default=list)
    played_cards = models.JSONField(default=list)
    duration_cards = models.JSONField(default=list)
    narnia_pile = models.JSONField(default=list)

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
    def real_hand(self):
        return get_cards_from_names(self.hand)

    @property
    def real_played_cards(self):
        return get_cards_from_names(self.played_cards)

    @property
    def real_narnia(self):
        return get_cards_from_names(self.narnia_pile)

    @property
    def score(self):
        return sum(card.get_victory_points(self) for card in self.all_cards)

    @property
    def no_actions(self):
        return list(card for card in self.real_hand if card.is_action) == []

    @property
    def no_treasure(self):
        return list(card for card in self.real_hand if card.is_treasure) == []

    def __len__(self):
        return len(self.all_cards)

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
            cards = self.real_hand

        for card in cards:
            self.discard_pile.append(self.hand.pop(self.hand.index(card.name)))

    def move_to_top_deck(self, card, source='hand'):
        card_source = getattr(self, source)
        card = card_source.pop(card_source.index(card.name))
        self.draw_pile.insert(0, card)

    def move_to_discard_pile(self, card, source='hand'):
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
            raise ValueError('invalid source')
        card_source = getattr(self, source)
        for card in cards:
            self.game.trash_pile.append(card.name)
            card_source.pop(card_source.index(card.name))
        self.save()
        self.game.save()

    def peek_deck(self, number=1):
        for _ in range(number):
            card = self.top_deck()
            if card is None:
                continue
            self.narnia_pile.append(card)
        result = self.narnia_pile[:]
        for card in self.narnia_pile:
            self.move_to_top_deck(card, 'narnia_pile')
        self.save()
        return result
