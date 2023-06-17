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
        for turn in stacked_turns:
            turn.is_current_turn = False
            turn.save()
            if turn.perform_simple_actions:
                deck = turn.game.decks.get(player=turn.player)
                turn.card.execute_card(deck, turn.turn)
                continue
            if turn.card.is_attack:
                if not turn.card.should_attack(turn):
                    continue
            adhocturn = turn.card.create_adhoc_turn(turn)
            if adhocturn:
                return adhocturn
        return None
