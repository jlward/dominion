from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from turns.models import Turn


@require_POST
def end_phase(request, turn_id):
    turn = get_object_or_404(Turn, pk=turn_id)
    if turn.state == 'action':
        turn.state = 'buy'
    if turn.state == 'buy':
        pass
    turn.save()
    turn.game.save()

    return redirect(request.META['HTTP_REFERER'])
