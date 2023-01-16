import uuid

from django.apps import apps
from django.db import models

from cards import get_cards_from_names_as_generator
from games.managers import GameManager


class Game(models.Model):
    objects = GameManager()

    players = models.ManyToManyField('players.Player')
    kingdom = models.JSONField(default=list)
    trash_pile = models.JSONField(default=list)
    game_hash = models.UUIDField()
    turn_order = models.JSONField(default=list)

    def save(self, *args, **kwargs):
        self.game_hash = uuid.uuid4()
        return super().save(*args, **kwargs)

    def create_turn(self, player):
        Turn = apps.get_model('turns', 'Turn')
        return Turn.objects.create(player=player, game=self, turn_number=1)

    def get_players(self, player):
        if player.pk not in self.turn_order:
            raise NotImplementedError()
        order = self.turn_order[:]
        while player.pk != order[0]:
            order.append(order.pop(0))

        return order

    def gain_card(self, deck, card):
        if self.kingdom[card.name] == 0:
            return
        deck.discard_pile.append(card.name)
        self.kingdom[card.name] -= 1

    @property
    def real_kingdom(self):
        kingdom = get_cards_from_names_as_generator(self.kingdom)
        result = {}
        for card in kingdom:
            result[card.name] = dict(card=card, count=self.kingdom[card.name])

        return result

    def get_current_turn(self):
        return self.turns.get(is_current_turn=True)
