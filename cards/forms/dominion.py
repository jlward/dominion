from django import forms

from .base import BaseCardForm


class ChapelForm(BaseCardForm):
    source_object = 'deck'
    source_pile = 'real_hand'
    actions = ['trash']
    min_cards = 0
    max_cards = 4


class CellarForm(BaseCardForm):
    source_object = 'deck'
    source_pile = 'real_hand'
    min_cards = 0
    max_cards = 1000

    def save(self):
        self.deck.discard_cards(self.cleaned_data['cards'])
        self.deck.draw_cards(len(self.cleaned_data['cards']))
        self.deck.save()
