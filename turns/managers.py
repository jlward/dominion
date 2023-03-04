from django.db import models


class TurnManager(models.Manager):
    pass


class AdHocTurnManager(models.Manager):
    def create(self, *args, **kwargs):
        game = kwargs['game']
        turns = self.filter(game=game, is_current_turn=True).order_by('turn_order')[1:]
        obj = super().create(*args, **kwargs)
        for i, turn in enumerate(turns):
            turn.turn_order = obj.turn_order + i + 1
            turn.save()

        return obj
