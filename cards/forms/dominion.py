from cards.forms.base.simple import SimpleForm
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
        if self.cleaned_data['selection'] != '0':
            return
        self.deck.trash_cards([Copper()])
        self.turn.available_money += 3
        self.deck.save()
        self.turn.save()


class FeastForm(ChooseCardsForm):
    source_object = 'game'
    source_pile = 'kingdom_options'
    min_cards = 1
    max_cards = 1

    def get_source_pile(self):
        source_pile = super().get_source_pile()
        return [card for card in source_pile if card.cost <= 5]

    def save(self):
        self.game.gain_card(self.deck, self.cleaned_data['cards'][0])
        self.deck.save()
        self.game.save()
