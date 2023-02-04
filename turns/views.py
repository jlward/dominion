from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from turns.models import AdHocTurn, Turn


@require_POST
def end_phase(request, turn_id):
    turn = get_object_or_404(Turn, pk=turn_id)
    if turn.state == 'action':
        turn.state = 'buy'
    elif turn.state == 'buy':
        turn.game.end_turn(turn)
        turn.state = 'end'
    turn.save()
    turn.game.save()

    return redirect(request.META['HTTP_REFERER'])


@require_POST
def perform_action(request, turn_id):
    turn = get_object_or_404(AdHocTurn, pk=turn_id)
    Form = turn.card.adhocturn_form
    deck = turn.game.decks.get(player=turn.player)
    form = Form(
        game=turn.game,
        player=turn.player,
        deck=deck,
        turn=turn.turn,
        data=request.POST,
    )
    if form.is_valid():
        form.save()
        turn.is_current_turn = False
        turn.save()
    return redirect(request.META['HTTP_REFERER'])
