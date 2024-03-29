from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from turns.models import Turn


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
def perform_action(request, Model, turn_id):
    turn = get_object_or_404(Model, pk=turn_id)
    Form = turn.form_class
    form = Form(data=request.POST, adhoc_turn=turn)
    if form.is_valid():
        form.save()
        turn.is_current_turn = False
        turn.save()
        turn.game.save()
    return redirect(request.META['HTTP_REFERER'])
