from django.test import TestCase

from games.models import Game
from players.factories import PlayerFactory


class GameTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.players = PlayerFactory.create_batch(2)

    def test_create_game_creates_a_game_with_everything_set(self):
        game = Game.objects.create_game(players=self.players)
        self.assertCountEqual(game.players.all(), self.players)
        default_kingdom_cards = [
            'Gold',
            'Silver',
            'Copper',
            'Province',
            'Duchy',
            'Estate',
            'Curse',
            'Smithy',
            'Village',
        ]
        self.assertEqual(game.kingdom, default_kingdom_cards)
        self.assertEqual(game.trash_pile, [])
        self.assertEqual(game.turn_order, [player.pk for player in self.players])
        assert game.game_hash
