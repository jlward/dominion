from django.db import models


class GameManger(models.Manager):
    default_kingdom_cards = [
        'Gold',
        'Silver',
        'Copper',
        'Province',
        'Duchy',
        'Estate',
        'Curse',
    ]

    def create_game(self, players):
        kingdom = self.default_kingdom_cards + ['Smithy', 'Village']
        turn_order = [player.pk for player in players]

        game = self.create(
            kingdom=kingdom,
            turn_order=turn_order,
        )
        game.players.set(players)
        return game
