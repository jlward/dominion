import random

from django.test import TestCase

from dominion.cards.models import Card
from dominion.decks.models import Deck
from dominion.games.factories import GameFactory
from dominion.games.models import Game
from dominion.players.factories import PlayerFactory


class AddPlayerTestCase(TestCase):
    def setUp(self):
        self.game = Game.objects.create()

    def test_add_player_adds_to_players(self):
        player = PlayerFactory()
        self.game.add_player(player)
        self.assertEqual(
            set(self.game.players.all()),
            set([player]),
        )

    def test_add_player_adds_player_to_player_order(self):
        players = PlayerFactory.create_batch(3)
        for player in players:
            self.game.add_player(player)
        self.assertEqual(
            set(self.game.player_order),
            set(player.pk for player in players),
        )

    def test_player_order_is_random(self):
        random.seed(8)
        player1 = PlayerFactory()
        player2 = PlayerFactory()
        player3 = PlayerFactory()
        player4 = PlayerFactory()

        # Player orders are always random.
        self.game.add_player(player1)
        self.assertEqual(
            self.game.player_order,
            [player1.pk],
        )

        self.game.add_player(player2)
        self.assertEqual(
            self.game.player_order,
            [player2.pk, player1.pk],
        )

        self.game.add_player(player3)
        self.assertEqual(
            self.game.player_order,
            [player1.pk, player2.pk, player3.pk],
        )

        self.game.add_player(player4)
        self.assertEqual(
            self.game.player_order,
            [player2.pk, player4.pk, player1.pk, player3.pk],
        )


class CreateCardInstanesTestCase(TestCase):
    def setUp(self):
        self.game = GameFactory()

    def test_one_query_per_card(self):
        # The query to get the list of cards.
        num_queries = Card.objects.count() + 1
        with self.assertNumQueries(num_queries):
            self.game.create_card_instances()

    def test_number_of_card_instances_created(self):
        self.game.create_card_instances()
        card_count = sum(Card.objects.values_list('count', flat=True))
        self.assertEqual(self.game.cardinstance_set.count(), card_count)


class StartGameTestCase(TestCase):
    def setUp(self):
        self.game = GameFactory()
        self.player = PlayerFactory()
        self.game.add_player(self.player)

    def test_deck_is_created_for_single_player(self):
        player = PlayerFactory()
        self.game.start()
        assert Deck.objects.get(game=self.game, player=self.player)
        with self.assertRaises(Deck.DoesNotExist):
            Deck.objects.get(game=self.game, player=player)

    def test_decks_are_created_for_players(self):
        player = PlayerFactory()
        self.game.add_player(player)
        self.game.start()
        assert Deck.objects.get(game=self.game, player=self.player)
        assert Deck.objects.get(game=self.game, player=player)

    def test_deck_size_is_set(self):
        self.game.start()
        deck = Deck.objects.get(game=self.game, player=self.player)
        self.assertEqual(deck.get_deck_size(), 10)
