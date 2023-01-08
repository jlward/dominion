from django.http import HttpResponse
from django.shortcuts import render

from games.models import Game
from players.models import Player


def game_state(request, game_id):
    if Player.objects.count() == 0:
        Player.objects.create(handle='Ward')
        Player.objects.create(handle='Probably D')

    try:
        game = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        players = Player.objects.all()
        game = Game.objects.create_game(players)

    context = dict(
        game=game,
    )
    return render(request, 'game_state.html', context)
