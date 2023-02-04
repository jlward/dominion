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
    def score(self):
        return sum(card.plus_victory_points for card in self.all_cards)

    def __len__(self):
        return len(self.all_cards)

    def draw_cards(self, num):
        for _ in range(num):
            if len(self.draw_pile) == 0:
                if len(self.discard_pile) == 0:
                    break
                self.full_shuffle()
            card = self.draw_pile.pop(0)
            self.hand.append(card)

    def play_card(self, card):
        self.hand.remove(card.name)
        self.played_cards.append(card.name)

    def cleanup(self):
        for _ in range(len(self.hand)):
            self.discard_pile.append(self.hand.pop())

        for _ in range(len(self.played_cards)):
            self.discard_pile.append(self.played_cards.pop())

    def full_shuffle(self):
        for _ in range(len(self.discard_pile)):
            self.draw_pile.append(self.discard_pile.pop())
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.draw_pile)

    # Assuming player can only trash from hand
    def trash_cards(self, cards):
        for card in cards:
            self.game.trash_pile.append(card.name)
            self.hand.pop(self.hand.index(card.name))
