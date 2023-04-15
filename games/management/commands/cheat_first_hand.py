import json

from django.core.management.base import BaseCommand

from games.models import Game
from players.models import Player

stub_template = {
    "kingdom_cards": ["Village"],
    "players": [
        {"hand": ["Thief"], "draw_pile": ["Gold", "Silver", "Smithy"]},
        {"hand": ["ThroneRoom", "Gold"]},
    ],
}


class Command(BaseCommand):
    advanced_file_name = 'advanced_cheat_command.json'

    def add_arguments(self, parser):
        parser.add_argument('kingdom_cards', type=str, nargs='*')
        parser.add_argument('--starting-money', type=int, default=0)
        parser.add_argument('--starting-buys', type=int, default=1)
        parser.add_argument('--keep-draw', action='store_true')
        parser.add_argument('--advanced', action='store_true')
        parser.add_argument('--create-stub-advanced-template', action='store_true')

    def do_advanced(self):
        with open(self.advanced_file_name) as f:
            data = json.loads(f.read())
        kingdom_cards = data['kingdom_cards']
        for player in data['players']:
            for value in player.values():
                kingdom_cards.extend(value)
        players = Player.objects.all()
        game = Game.objects.create_game(players, kingdom_cards)
        game.create_turn(players[0])
        for player, deck in zip(data['players'], game.decks.all()):
            for key, value in player.items():
                setattr(deck, key, value)
            deck.save()
        print(game.pk)

    def handle(self, *args, **options):
        if options['create_stub_advanced_template']:
            with open(self.advanced_file_name, 'w') as f:
                f.write(json.dumps(stub_template, indent=4))
            return

        if options['advanced']:
            self.do_advanced()
            return
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
