from django import forms
from django.utils.safestring import mark_safe

from cards import get_cards_from_names


class SimpleForm(forms.Form):
    selection = forms.ChoiceField(
        choices=['Yes', 'No'],
        widget=forms.RadioSelect(),
    )

    def __init__(self, game, player, deck, turn, *args, **kwargs):
        self.game = game
        self.player = player
        self.deck = deck
        self.turn = turn
        super().__init__(*args, **kwargs)

    def save(self):
        raise NotImplementedError()
