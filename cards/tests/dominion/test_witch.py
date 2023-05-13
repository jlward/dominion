from django.test import TestCase

from cards.kingdom_cards.dominion import Witch
from games.factories import GameFactory
from players.factories import PlayerFactory
from turns.factories import TurnFactory


class WitchCardTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Witch()

    def assert_witch(self):
        self.game.refresh_from_db()
        self.deck.refresh_from_db()

        self.assertNotIn('Curse', self.deck.discard_pile)
        self.assertEqual(self.game.kingdom['Curse'], 0)

        order = self.game.get_players(self.player)
        self.assertEqual(self.player.pk, order.pop(0))

        no_curse = order.pop()
        no_curse_deck = self.game.decks.get(player_id=no_curse)
        self.assertNotIn('Curse', no_curse_deck.discard_pile)

        for player_id in order:
            player_deck = self.game.decks.get(player_id=player_id)
            self.assertIn('Curse', player_deck.discard_pile)

    def test_perform_specific_action(self):
        self.card.perform_specific_actions(deck=self.deck, turn=self.turn)
        self.assert_witch()
