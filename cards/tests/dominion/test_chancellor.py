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
        with self.assert_stacked_turn_created(2):
            stacked_turns = self.card.create_stacked_turns(
                deck=self.deck,
                turn=self.turn,
            )
        stacked_turn = stacked_turns[0]
        self.assert_stacked_turn(
            stacked_turn=stacked_turn,
            turn=self.turn,
            player=self.player,
            game=self.game,
            card=self.card,
        )
        stacked_turn = stacked_turns[1]
        self.assert_stacked_turn(
            stacked_turn=stacked_turn,
            turn=self.turn,
            player=self.player,
            game=self.game,
            card=self.card,
            perform_simple_actions=True,
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

    def test_decline_deck_to_discard(self):
        discard = self.deck.discard_pile[:]
        draw = self.deck.draw_pile[:]
        form = self.build_card_form(
            adhoc_turn=self.adhoc_turn,
            selection=self.card.adhocturn_form.selection_no,
        )
        assert form.is_valid()
        form.save()
        self.deck.refresh_from_db()
        self.assertEqual(self.deck.discard_pile, discard)
        self.assertEqual(self.deck.draw_pile, draw)

    def test_accept_deck_to_discard(self):
        discard = self.deck.discard_pile[:]
        draw = self.deck.draw_pile[:]
        form = self.build_card_form(
            adhoc_turn=self.adhoc_turn,
            selection=self.card.adhocturn_form.selection_yes,
        )
        assert form.is_valid()
        form.save()
        self.deck.refresh_from_db()
        self.assertEqual(self.deck.discard_pile, discard + draw)
        self.assertEqual(self.deck.draw_pile, [])
