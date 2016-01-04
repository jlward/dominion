import random

from django.db import models

from jsonfield import JSONField

from dominion.cards.models import CardInstance


class Deck(models.Model):
    game = models.ForeignKey('games.Game')
    player = models.ForeignKey('players.Player')
    deck_order = JSONField(default=[])
    current_hand = JSONField(default=[])

    def get_starting_cards(self):
        card_pks = list(CardInstance.objects.filter(
            game=self.game,
            card__name='copper',
            deck=None,
        ).values_list(
            'pk',
            flat=True,
        )[:7])
        card_pks += list(CardInstance.objects.filter(
            game=self.game,
            card__name='estate',
            deck=None,
        ).values_list(
            'pk',
            flat=True,
        )[:3])
        CardInstance.objects.filter(
            pk__in=card_pks,
        ).update(
            deck=self,
        )
        self.shuffle_deck()

    @property
    def cards(self):
        if hasattr(self, '_cards'):
            return self._cards
        self._cards = list(self.cardinstance_set.all())
        return self._cards

    def get_deck_size(self):
        return len(self.cards)

    def shuffle_deck(self):
        self.deck_order = list(card.pk for card in self.cards)
        random.shuffle(self.deck_order)
        self.save()

    def draw_hand(self):
        self.current_hand = self.deck_order[:5]
        self.deck_order = self.deck_order[5:]
        self.save()
