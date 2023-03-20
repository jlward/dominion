from cards.kingdom_cards.dominion import Chancellor
from games.factories import GameFactory
from players.factories import PlayerFactory
from testing import BaseTestCase
from turns.factories import AdHocTurnFactory, TurnFactory


class ChancellorCardTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Chancellor()

    def test_perform_specific_action(self):
        with self.assert_adhoc_turn_created():
            adhoc_turn = self.card.perform_specific_action(
                deck=self.deck,
                turn=self.turn,
            )
        self.assert_adhoc_turn(
            adhoc_turn=adhoc_turn,
            turn=self.turn,
            player=self.player,
            game=self.game,
            card=self.card,
        )


# form.save() does nothing
# these tests don't work. they do nothing at all. they don't seem to enter the save() of the form. missing some major piece here..
class ChancellorFormTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.game = GameFactory(players=[self.player] + PlayerFactory.create_batch(11))
        self.turn = TurnFactory(player=self.player, game=self.game)
        self.deck = self.game.decks.get(player=self.player)
        self.card = Chancellor()
        self.adhoc_turn = AdHocTurnFactory(
            player=self.player,
            game=self.game,
            turn=self.turn,
            card=self.card,
        )

    def test_deck_not_in_discard(self):
        discard = self.deck.discard_pile[:]
        draw = self.deck.draw_pile[:]
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, selection='1')
        assert form.is_valid()
        form.save()
        self.deck.refresh_from_db()
        self.assertEqual(self.deck.discard_pile, discard)
        self.assertEqual(self.deck.draw_pile, draw)

    def test_deck_in_discard(self):
        discard = self.deck.discard_pile[:]
        draw = self.deck.draw_pile[:]
        form = self.build_card_form(adhoc_turn=self.adhoc_turn, selection='0')
        assert form.is_valid()
        form.save()
        self.deck.refresh_from_db()
        self.assertEqual(self.deck.discard_pile, discard + draw)
        self.assertEqual(self.deck.draw_pile, [])
