from django import forms


class SimpleForm(forms.Form):
    selection = forms.ChoiceField(
        choices=[
            (0, 'Yes'),
            (1, 'No'),
        ],
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
