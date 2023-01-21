from django import forms

from players.models import Player


class GameCreateForm(forms.Form):
    player = forms.ModelChoiceField(queryset=None)

    def __init__(self, player, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['player'].queryset = Player.objects.exclude(
            pk=player.pk,
        )
