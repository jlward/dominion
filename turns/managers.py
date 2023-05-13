from django.apps import apps
from django.db import models


class TurnManager(models.Manager):
    pass


class AdHocTurnManager(models.Manager):
    pass


class StackedTurnManager(models.Manager):
    def process_for_game(self, game):
        stacked_turns = game.stackedturns.filter(is_current_turn=True).order_by(
            '-turn_order',
        )
        AdHocTurn = apps.get_model('turns', 'AdHocTurn')
        for turn in stacked_turns:
            turn.is_current_turn = False
            turn.save()
            if turn.perform_simple_actions:
                deck = turn.game.decks.get(player=turn.player)
                turn.card.perform_simple_actions(deck, turn.turn)
                continue
            if turn.card.should_create_adhoc_turn(turn):
                return AdHocTurn.objects.create(
                    turn=turn.turn,
                    player=turn.player,
                    game=turn.game,
                    card=turn.card,
                    target_player=turn.target_player,
                    card_form_field_string=turn.card_form_field_string,
                    card_form_title_field_string=turn.card_form_title_field_string,
                )
        return None
