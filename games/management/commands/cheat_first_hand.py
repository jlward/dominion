from django.core.management.base import BaseCommand

from games.models import Game
from players.models import Player


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('kingdom_cards', type=str, nargs='+')

    def handle(self, *args, **options):
        kingdom_cards = options['kingdom_cards']
        players = Player.objects.all()
        game = Game.objects.create_game(players, kingdom_cards)
        game.create_turn(players[0])
        for deck in game.decks.all():
            deck.draw_pile = []
            deck.hand = kingdom_cards
            deck.save()
        print(game.pk)
