from django import forms
from django.utils.safestring import mark_safe

from cards import get_cards_from_names


class BaseCardForm(forms.Form):
    cards = forms.MultipleChoiceField(
        choices=[],
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'kingdom-selector',
            },
        ),
    )
    source_object = None
    source_pile = None
    action = None
    min_cards = 1
    max_cards = 1

    def __init__(self, game, player, deck, turn, *args, **kwargs):
        self.game = game
        self.player = player
        self.deck = deck
        self.turn = turn
        super().__init__(*args, **kwargs)
        source_object = getattr(self, self.source_object)
        source_pile = getattr(source_object, self.source_pile)
        self.fields['cards'].choices = [
            (card.name, mark_safe(f'<img src="{card.url}" />')) for card in source_pile
        ]

    def save(self):
        if self.action == 'trash':
            self.game.trash_cards(
                deck=self.deck,
                turn=self.turn,
                cards=self.cleaned_data['cards'],
            )
        else:
            raise NotImplementedError()

    def clean_cards(self):
        cards = self.cleaned_data['cards']

        if len(cards) < self.min_cards:
            raise forms.ValidationError(f'You selected less than {self.min_cards}')
        if len(cards) > self.max_cards:
            raise forms.ValidationError(f'You selected more than {self.max_cards}')

        self.cleaned_data['cards'] = get_cards_from_names(cards)
        return self.cleaned_data['cards']
