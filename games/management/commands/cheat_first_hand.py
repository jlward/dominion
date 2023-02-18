from django.core.management.base import BaseCommand

from games.models import Game
from players.models import Player


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('kingdom_cards', type=str, nargs='+')
        parser.add_argument('--starting-money', type=int, default=0)
        parser.add_argument('--starting-buys', type=int, default=1)
        parser.add_argument('--keep-draw', action='store_true')

    def handle(self, *args, **options):
        kingdom_cards = options['kingdom_cards']
        players = Player.objects.all()
        game = Game.objects.create_game(players, kingdom_cards)
        turn = game.create_turn(players[0])
        turn.available_buys = options['starting_buys']
        turn.available_money = options['starting_money']
        turn.save()
        for deck in game.decks.all():
            if not options['keep_draw']:
                deck.draw_pile = []
            deck.hand = kingdom_cards
            deck.save()
        print(game.pk)
