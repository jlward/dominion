from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

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
        game.create_turn(players[0])

    context = dict(
        game=game,
    )
    return render(request, 'game_state.html', context)


def play_game_as_player(request, game_id, player_id):
    game = get_object_or_404(
        Game,
        pk=game_id,
    )
    player = get_object_or_404(
        Player,
        pk=player_id,
    )
    deck = game.decks.get(player=player)
    turn = game.get_current_turn()
    if turn.player_id != player.pk:
        turn = None

    context = dict(
        game=game,
        player=player,
        deck=deck,
        turn=turn,
    )
    return render(request, 'play_game_as_player.html', context)
