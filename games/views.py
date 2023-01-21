from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from games.forms import GameCreateForm
from games.models import Game
from players.models import Player


@login_required
def game_list(request):
    form = GameCreateForm(request.user.player)
    games = Game.objects.all()
    context = dict(
        games=games,
        form=form,
    )
    return render(request, 'game_list.html', context)


@login_required
@require_POST
def game_create(request):
    form = GameCreateForm(
        request.user.player,
        data=request.POST,
    )
    if not form.is_valid():
        return redirect('game_list')

    players = [request.user.player, form.cleaned_data['player']]
    game = Game.objects.create_game(
        players=players,
        kingdom=form.cleaned_data['kingdom'],
    )
    game.create_turn(players[0])
    return redirect('games_play', game_id=game.pk)


@login_required
def game_state(request, game_id):
    game = get_object_or_404(
        Game,
        pk=game_id,
    )

    context = dict(
        game=game,
    )
    return render(request, 'game_state.html', context)


@login_required
def play_game_as_player(request, game_id):
    game = get_object_or_404(
        Game,
        pk=game_id,
    )
    player = request.user.player
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
