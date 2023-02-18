from django import forms
from django.utils.safestring import mark_safe

from cards import get_cards_from_names


class ChooseCardsForm(forms.Form):
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
    actions = None
    min_cards = 1
    max_cards = 1

    def __init__(self, adhoc_turn, *args, **kwargs):
        self.game = adhoc_turn.game
        self.player = adhoc_turn.player
        self.deck = self.game.decks.get(player=self.player)
        self.turn = adhoc_turn.turn
        self.adhoc_turn = adhoc_turn
        super().__init__(*args, **kwargs)
        source_pile = self.get_source_pile()
        self.fields['cards'].choices = [
            (card.name, mark_safe(f'<img src="{card.url}" />')) for card in source_pile
        ]

    def save(self):
        action_performed = False
        if 'trash' in self.actions:
            self.game.trash_cards(
                deck=self.deck,
                turn=self.turn,
                cards=self.cleaned_data['cards'],
            )
            action_performed = True
        if not action_performed:
            raise NotImplementedError()

    def clean_cards(self):
        cards = self.cleaned_data['cards']

        if len(cards) < self.min_cards:
            raise forms.ValidationError(f'You selected less than {self.min_cards}')
        if len(cards) > self.max_cards:
            raise forms.ValidationError(f'You selected more than {self.max_cards}')

        self.cleaned_data['cards'] = get_cards_from_names(cards)
        return self.cleaned_data['cards']

    def get_source_pile(self):
        source_object = getattr(self, self.source_object)
        return getattr(source_object, self.source_pile)
