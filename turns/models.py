from django.apps import apps
from django.db import models

from turns.managers import TurnManager


class Turn(models.Model):
    objects = TurnManager()

    player = models.ForeignKey(
        'players.Player',
        related_name='turns',
        on_delete=models.PROTECT,
    )
    game = models.ForeignKey(
        'games.Game',
        related_name='turns',
        on_delete=models.PROTECT,
    )
    turn_number = models.IntegerField()
    is_current_turn = models.BooleanField(default=True, db_index=True)
    # Standard card stuff
    available_actions = models.IntegerField(default=1)
    available_buys = models.IntegerField(default=1)
    available_money = models.IntegerField(default=0)

    # What cards were played
    actions_played = models.JSONField(default=list)
    # What cards were trashed
    cards_trashed = models.JSONField(default=list)
    # Who played what reaction card
    reactions_played = models.JSONField(default=list)
    # End of turn stuff
    treasures_played = models.JSONField(default=list)
    buys_used = models.JSONField(default=list)
    cards_bought = models.JSONField(default=list)
    cards_gained = models.JSONField(default=list)

    class Meta:
        index_together = [
            ('game', 'is_current_turn'),
        ]

    def play_action(self, action):
        Deck = apps.get_model('decks', 'Deck')
        player_deck = Deck.objects.get(game_id=self.game_id, player_id=self.player_id)
        player_deck.play_card(action)
        self.actions_played.append(action.name)
        action.perform_action(deck=player_deck, turn=self)
        self.available_actions -= 1
        player_deck.save()
        self.save()

    def play_treasures(self, treasures):
        self.treasures_played.extend(treasure.name for treasure in treasures)
        self.available_money += sum(treasure.plus_treasures for treasure in treasures)
        self.save()

    def perform_buy(self, kingdom_card):
        game = self.game
        Deck = apps.get_model('decks', 'Deck')
        player_deck = Deck.objects.get(game_id=self.game_id, player_id=self.player_id)
        player_deck.discard_pile.append(kingdom_card.name)
        game.kingdom[kingdom_card.name] -= 1
        self.available_buys -= 1
        self.available_money -= kingdom_card.cost
        game.save()
        player_deck.save()
        self.save()

    def perform_cleanup(self):
        pass
