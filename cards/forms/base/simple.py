from django import forms


class SimpleForm(forms.Form):
    selection_yes = '1'
    selection_no = '0'
    selection = forms.ChoiceField(
        choices=[
            (selection_yes, 'Yes'),
            (selection_no, 'No'),
        ],
        widget=forms.RadioSelect(),
    )

    def __init__(self, adhoc_turn, *args, **kwargs):
        self.game = adhoc_turn.game
        self.player = adhoc_turn.player
        self.deck = self.game.decks.get(player=self.player)
        self.turn = adhoc_turn.turn
        self.adhoc_turn = adhoc_turn
        super().__init__(*args, **kwargs)

    def save(self):  # pragma: no cover
        raise NotImplementedError()
