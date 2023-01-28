from django import forms
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from cards import get_all_cards, get_available_kingdom_cards
from players.models import Player


class GameCreateForm(forms.Form):
    player = forms.ModelChoiceField(queryset=None)
    kingdom = forms.MultipleChoiceField(
        choices=[
            (name, mark_safe(f'<img src="{card().url}" />'))
            for name, card in get_available_kingdom_cards().items()
        ],
        widget=forms.CheckboxSelectMultiple(
            attrs={
                'class': 'kingdom-selector',
            },
        ),
    )

    def __init__(self, player, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['player'].queryset = Player.objects.exclude(
            pk=player.pk,
        )


class PlayTreasureForm(forms.Form):
    card = forms.ChoiceField()

    def __init__(self, data, deck, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self.fields['card'].choices = [(card, card) for card in deck.hand]

    def clean_card(self):
        card = self.cleaned_data['card']
        all_cards = get_all_cards()
        self.cleaned_data['card'] = all_cards[card]()
        return self.cleaned_data['card']
