from django.db import models


class Deck(models.Model):
    game = models.ForeignKey('games.Game', related_name='decks')
    player = models.ForeignKey('players.Player', related_name='decks')

    draw_pile = models.JSONField(default=list)
    discard_pile = models.JSONField(default=list)
    hand = models.JSONField(default=list)
    played_cards = models.JSONField(default=list)
    duration_cards = models.JSONField(default=list)

    @property
    def all_cards(self):
        return (
            self.draw_pile
            + self.discard_pile
            + self.hand
            + self.duration_cards
            + self.played_cards
        )

    def __len__(self):
        return len(self.all_cards)
