from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from games.forms import BuyKingdomCard, GameCreateForm, PlayActionForm, PlayTreasureForm
from games.models import Game


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
    if turn and turn.player_id != player.pk:
        turn = None

    context = dict(
        game=game,
        player=player,
        deck=deck,
        turn=turn,
    )
    return render(request, 'play_game_as_player.html', context)


@login_required
@require_POST
def play_action(request, game_id):
    game = get_object_or_404(
        Game,
        pk=game_id,
    )
    player = request.user.player
    deck = game.decks.get(player=player)
    turn = game.get_current_turn()
    form = PlayActionForm(request.POST, deck)
    if form.is_valid():
        turn.play_action(form.cleaned_data['card'])
        game.save()
        return JsonResponse(dict(okay=True))

    return JsonResponse(dict(okay=False))


@login_required
@require_POST
def play_treasure(request, game_id):
    game = get_object_or_404(
        Game,
        pk=game_id,
    )
    player = request.user.player
    deck = game.decks.get(player=player)
    turn = game.get_current_turn()
    form = PlayTreasureForm(request.POST, deck)
    if form.is_valid():
        deck.play_card(form.cleaned_data['card'])
        turn.play_treasures([form.cleaned_data['card']])
        deck.save()
        game.save()
        return JsonResponse(dict(okay=True))

    return JsonResponse(dict(okay=False))


@login_required
@require_POST
def play_all_treasures(request, game_id):
    game = get_object_or_404(
        Game,
        pk=game_id,
    )
    player = request.user.player
    deck = game.decks.get(player=player)
    turn = game.get_current_turn()
    cards = [card for card in deck.real_hand if card.is_treasure]
    for card in cards:
        deck.play_card(card)
    turn.play_treasures(cards)
    deck.save()
    game.save()

    return redirect(request.META['HTTP_REFERER'])


@login_required
@require_POST
def buy_kingdom_card(request, game_id):
    game = get_object_or_404(
        Game,
        pk=game_id,
    )
    turn = game.get_current_turn()
    form = BuyKingdomCard(request.POST, game, turn)
    if form.is_valid():
        turn.perform_buy(form.cleaned_data['card'])
        return JsonResponse(dict(okay=True))

    return JsonResponse(dict(okay=False))


@login_required
def game_hash(request, game_id):
    game = get_object_or_404(
        Game,
        pk=game_id,
    )

    return JsonResponse(dict(hash=game.game_hash))
