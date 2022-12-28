import random

from django.db import models


class DeckManager(models.Manager):
    default_draw_pile = [
        'Copper',
        'Copper',
        'Copper',
        'Copper',
        'Copper',
        'Copper',
        'Copper',
        'Estate',
        'Estate',
        'Estate',
    ]

    def create_deck(self, game, player):
        game.kingdom['Copper'] -= 7
        default_draw_pile = self.default_draw_pile[:]
        random.shuffle(default_draw_pile)
        return self.create(
            game=game,
            player=player,
            draw_pile=default_draw_pile[:5],
            hand=default_draw_pile[5:],
        )
