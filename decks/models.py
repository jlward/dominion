import random

from django.db import models

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
        return (
            self.draw_pile
            + self.discard_pile
            + self.hand
            + self.duration_cards
            + self.played_cards
        )

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

    def full_shuffle(self):
        for _ in range(len(self.discard_pile)):
            self.draw_pile.append(self.discard_pile.pop())
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.draw_pile)
