from django.apps import apps
from django.db import models

from cards.fields import CardField
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
    state = models.CharField(
        choices=[('action', 'Action Phase'), ('buy', 'Buy Phase')],
        default='action',
        max_length=10,
    )
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

    @property
    def is_action_phase(self):
        return self.state == 'action'

    def get_deck(self):
        Deck = apps.get_model('decks', 'Deck')
        return Deck.objects.get(game_id=self.game_id, player_id=self.player_id)

    def play_action(self, action):
        player_deck = self.get_deck()
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
        player_deck = self.get_deck()
        game.gain_card(player_deck, kingdom_card)
        self.available_buys -= 1
        self.available_money -= kingdom_card.cost
        game.save()
        player_deck.save()
        self.save()

    def perform_cleanup(self):
        player_deck = self.get_deck()
        player_deck.cleanup()
        player_deck.draw_cards(5)
        player_deck.save()
        self.is_current_turn = False
        self.save()


class AdHocTurn(models.Model):
    turn = models.ForeignKey(
        'turns.Turn',
        related_name='adhoc_turns',
        on_delete=models.PROTECT,
    )
    player = models.ForeignKey(
        'players.Player',
        related_name='adhoc_turns',
        on_delete=models.PROTECT,
    )
    game = models.ForeignKey(
        'games.Game',
        related_name='adhoc_turns',
        on_delete=models.PROTECT,
    )
    is_current_turn = models.BooleanField(default=True, db_index=True)
    card = CardField()
