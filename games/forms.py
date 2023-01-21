from django import forms
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from cards import get_available_kingdom_cards
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
