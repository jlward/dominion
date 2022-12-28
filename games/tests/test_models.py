from django.test import TestCase

from decks.models import Deck
from games.factories import GameFactory
from games.models import Game
from players.factories import PlayerFactory


class GameTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.players = PlayerFactory.create_batch(2)

    def test_create_game_creates_a_game_with_everything_set(self):
        game = Game.objects.create_game(players=self.players)
        self.assertCountEqual(game.players.all(), self.players)
        default_kingdom_cards = dict(
            Gold=1000,
            Silver=1000,
            Copper=986,
            # This is wrong for two players
            Province=10,
            # This is wrong for two players
            Duchy=10,
            # This is wrong for two players
            Estate=10,
            Curse=10,
            Smithy=10,
            Village=10,
        )
        self.assertEqual(game.kingdom, default_kingdom_cards)
        self.assertEqual(game.trash_pile, [])
        self.assertEqual(game.turn_order, [player.pk for player in self.players])
        assert game.game_hash

        for player in self.players:
            deck = Deck.objects.get(
                game=game,
                player=player,
            )
            self.assertEqual(len(deck.draw_pile), 5)
            self.assertEqual(len(deck.hand), 5)
            self.assertCountEqual(
                deck.draw_pile + deck.hand,
                Deck.objects.default_draw_pile,
            )

    def test_create_turn(self):
        game = GameFactory()
        turn = game.create_turn(player=self.players[0])
        self.assertEqual(turn.player, self.players[0])
        self.assertEqual(turn.game, game)
        self.assertEqual(turn.turn_number, 1)
