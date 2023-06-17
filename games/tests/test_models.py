from unittest import mock

from cards.kingdom_cards.base_cards import Copper, Curse
from decks.models import Deck
from games.factories import GameFactory
from games.models import Game
from players.factories import PlayerFactory
from testing import BaseTestCase


class GameTestCase(BaseTestCase):
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

    def test_get_players(self):
        game = self.create_game(players=self.players)
        player1, player2 = self.players
        self.assertEqual(game.get_players(player1), [player1.pk, player2.pk])
        self.assertEqual(game.get_players(player2), [player2.pk, player1.pk])

    def test_kingdom_options(self):
        game = self.create_game(players=self.players, kingdom_cards=['Village'])
        expected = [
            'Gold',
            'Silver',
            'Copper',
            'Province',
            'Duchy',
            'Estate',
            'Curse',
            'Village',
        ]
        self.assertEqual(list(card.name for card in game.kingdom_options), expected)

        game.kingdom['Village'] = 0

        expected = ['Gold', 'Silver', 'Copper', 'Province', 'Duchy', 'Estate', 'Curse']
        self.assertEqual(list(card.name for card in game.kingdom_options), expected)

    def test_winner(self):
        game = self.create_game(players=self.players, kingdom_cards=['Village'])
        self.assertEqual(game.winner, '-')
        game.is_over = True
        self.assertEqual(game.winner, self.players[0])

    def test_get_current_turn(self):
        game = self.create_game(players=self.players, kingdom_cards=['Village'])
        game.is_over = True
        self.assertEqual(game.get_current_turn(), None)

    def test_end_turn(self):
        game = self.create_game(players=self.players, kingdom_cards=['Village'])
        turn = game.get_current_turn()
        with mock.patch('turns.models.Turn.perform_cleanup') as perform_cleanup:
            with mock.patch('games.models.Game.create_turn') as create_turn:
                game.end_turn(turn)
        perform_cleanup.assert_called_once()
        create_turn.assert_called_once()

    def test_check_game_over_province(self):
        game = self.create_game(players=self.players, kingdom_cards=['Village'])
        game.kingdom['Province'] = 0
        self.assertEqual(game.is_over, False)
        game.check_game_over()
        self.assertEqual(game.is_over, True)

    def test_check_game_over_piles(self):
        game = self.create_game(players=self.players, kingdom_cards=['Village'])

        game.check_game_over()
        self.assertEqual(game.is_over, False)

        game.kingdom['Village'] = 0
        game.check_game_over()
        self.assertEqual(game.is_over, False)

        game.kingdom['Estate'] = 0
        game.check_game_over()
        self.assertEqual(game.is_over, False)

        game.kingdom['Duchy'] = 0
        game.check_game_over()
        self.assertEqual(game.is_over, True)

    def test_move_cards_from_narnias_to_player_card_not_in_narnia(self):
        game = self.create_game(players=self.players, kingdom_cards=['Village'])
        game.move_cards_from_narnias_to_player(
            [Copper],
            self.players[0],
            destination='discard_pile',
        )
        for deck in game.decks.all():
            self.assertEqual(deck.discard_pile, [])
        game.move_cards_from_narnias_to_player(
            [],
            self.players[0],
            destination='discard_pile',
        )
        for deck in game.decks.all():
            self.assertEqual(deck.discard_pile, [])

    def test_gain_card_from_empty_pile(self):
        game = self.create_game(players=self.players, kingdom_cards=['Village'])
        deck = game.decks.first()
        for _ in range(11):
            game.gain_card(deck, Curse())
        self.assertEqual(len(deck.discard_pile), 10)
