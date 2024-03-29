from django.apps import apps
from django.db import models
from django.urls import reverse

from cards.constants import CardTypes
from cards.fields import CardField
from turns.managers import AdHocTurnManager, StackedTurnManager, TurnManager


class BaseTurn(models.Model):
    player = models.ForeignKey(
        'players.Player',
        related_name='%(class)ss',
        on_delete=models.PROTECT,
    )
    game = models.ForeignKey(
        'games.Game',
        related_name='%(class)ss',
        on_delete=models.PROTECT,
    )
    is_current_turn = models.BooleanField(default=True, db_index=True)

    class Meta:
        abstract = True


class Turn(BaseTurn):
    objects = TurnManager()

    state = models.CharField(
        choices=[('action', 'Action Phase'), ('buy', 'Buy Phase')],
        default='action',
        max_length=10,
    )
    turn_number = models.IntegerField()
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

    def get_deck(self):
        Deck = apps.get_model('decks', 'Deck')
        return Deck.objects.get(game_id=self.game_id, player_id=self.player_id)

    def play_action(self, action, consume=True, ghost_action=False):
        player_deck = self.get_deck()
        if action.is_attack:
            opponent_decks = self.game.get_decks(self.player)
            for deck in opponent_decks:
                if deck.no_reactions:
                    continue
                reactions = deck.get_cards_of_type(CardTypes.Reaction)
                for reaction in reactions:
                    ReactionTurn.objects.create(
                        card=action,
                        reaction_card=reaction,
                        turn=self,
                        player=deck.player,
                        game=self.game,
                    )

        if not ghost_action:
            player_deck.play_card(action)
        self.actions_played.append(action.name)
        action.play_action(deck=player_deck, turn=self)
        if consume:
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

    def trash_cards(self, cards):
        self.cards_trashed.extend(card.name for card in cards)
        self.save()

    def perform_cleanup(self):
        player_deck = self.get_deck()
        player_deck.cleanup()
        player_deck.draw_cards(5)
        player_deck.save()
        self.is_current_turn = False
        self.save()


class BaseTempTurn(models.Model):
    card = CardField()
    turn = models.ForeignKey(
        'turns.Turn',
        related_name='%(class)ss',
        on_delete=models.PROTECT,
    )
    target_player = models.ForeignKey(
        'players.Player',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
    )
    turn_order = models.IntegerField(default=0)
    card_form_field_string = models.CharField(max_length=250, default='adhocturn_form')
    card_form_title_field_string = models.CharField(
        max_length=250,
        default='adhocturn_action_title',
    )

    def save(self, *args, **kwargs):
        if not self.pk:
            # if we delete any adhoc turns this will break
            self.turn_order = self.__class__.objects.count() + 1
        return super().save(*args, **kwargs)

    def get_target_player_deck(self):
        return self.game.decks.get(player=self.target_player)


class AdHocTurn(BaseTempTurn, BaseTurn):
    objects = AdHocTurnManager()

    @property
    def form_class(self):
        return getattr(self.card, self.card_form_field_string)

    @property
    def form(self):
        return self.form_class(
            adhoc_turn=self,
        )

    @property
    def perform_action_url(self):
        return reverse(
            'turns_adhocturn_adhoc_perform_action',
            kwargs=dict(turn_id=self.pk),
        )

    def get_form_title(self):
        return getattr(self.card, self.card_form_title_field_string)


class StackedTurn(BaseTempTurn, BaseTurn):
    perform_simple_actions = models.BooleanField(default=False)
    objects = StackedTurnManager()


class ReactionTurn(BaseTempTurn, BaseTurn):
    reaction_card = CardField()
    response = models.BooleanField(default=None, null=True, blank=True)

    @property
    def perform_action_url(self):
        return reverse(
            'turns_adhocturn_reaction_perform_action',
            kwargs=dict(turn_id=self.pk),
        )

    @property
    def form_class(self):
        return getattr(self.reaction_card, self.card_form_field_string)

    @property
    def form(self):
        return self.form_class(
            adhoc_turn=self,
        )
