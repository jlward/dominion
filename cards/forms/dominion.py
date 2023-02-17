from django import forms

from cards.forms.base.binary import SimpleForm
from cards.kingdom_cards.base_cards import Copper

from .base.choose_cards import ChooseCardsForm


class ChapelForm(ChooseCardsForm):
    source_object = 'deck'
    source_pile = 'real_hand'
    actions = ['trash']
    min_cards = 0
    max_cards = 4


class CellarForm(ChooseCardsForm):
    source_object = 'deck'
    source_pile = 'real_hand'
    min_cards = 0
    max_cards = 1000

    def save(self):
        self.deck.discard_cards(self.cleaned_data['cards'])
        self.deck.draw_cards(len(self.cleaned_data['cards']))
        self.deck.save()


class MoneylenderForm(SimpleForm):
    def save(self):
        if self.cleaned_data['selection'] == 'Yes':
            self.deck.trash_cards(Copper())
            self.turn.available_money += 3
            self.deck.save()
            self.turn.save()
