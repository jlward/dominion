import uuid

from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
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
    is_over = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.check_game_over()
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

    def trash_cards(self, deck, turn, cards):
        deck.trash_cards(cards)
        turn.trash_cards(cards)
        deck.save()
        self.save()

    @property
    def real_kingdom(self):
        kingdom = get_cards_from_names_as_generator(self.kingdom)
        result = {}
        for card in kingdom:
            count = self.kingdom[card.name]
            if card.unlimited:
                count = '∞'
            result[card.name] = dict(card=card, count=count)

        return result

    @property
    def real_base_kingdom(self):
        kingdom = self.real_kingdom
        result = [row for row in kingdom.values() if row['card'].is_base_card]
        return result

    @property
    def real_not_base_kingdom(self):
        kingdom = self.real_kingdom
        result = [row for row in kingdom.values() if not row['card'].is_base_card]
        return result

    @property
    def winner(self):
        if not self.is_over:
            return '-'
        score = -1000
        winner = None
        for deck in self.decks.all():
            if deck.score > score:
                winner = deck.player
                score = deck.score
                # TODO make ties work
        return winner

    def get_current_turn(self):
        if self.is_over:
            return None

        try:
            adhoc_turn = self.adhoc_turns.get(is_current_turn=True)
            return adhoc_turn
        except ObjectDoesNotExist:
            pass

        return self.turns.get(is_current_turn=True)

    def end_turn(self, turn):
        turn.perform_cleanup()
        players = self.get_players(turn.player)
        Player = apps.get_model('players', 'Player')
        self.create_turn(Player(pk=players[1]))
        self.save()

    def check_game_over(self):
        if self.kingdom['Province'] < 1:
            self.is_over = True
        if len([count for count in self.kingdom.values() if count < 1]) > 2:
            self.is_over = True
