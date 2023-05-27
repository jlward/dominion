from collections import Counter
from contextlib import contextmanager

from django.test import TestCase
from faker import Faker

from cards import get_cards_from_names
from cards.forms.base.simple import SimpleForm
from games.models import Game
from players.factories import PlayerFactory
from turns.models import AdHocTurn, StackedTurn


class BaseTestCase(TestCase):
    faker = Faker()
    SELECTION_YES = SimpleForm.selection_yes
    SELECTION_NO = SimpleForm.selection_no
    auto_login_player = True

    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        if self.auto_login_player:
            self.client.force_login(self.player.user)

    def create_game(self, players=None, kingdom_cards=None):
        if kingdom_cards is None:
            kingdom_cards = ['Village', 'Smithy']
        if players is None:
            players = PlayerFactory.create_batch(2)
        game = Game.objects.create_game(players, kingdom_cards)
        game.create_turn(players[0])
        return game

    @contextmanager
    def assert_stacked_turn_created(self, count=1):
        before_turn_count = StackedTurn.objects.count()
        yield
        after_turn_count = StackedTurn.objects.count()
        self.assertEqual(after_turn_count, before_turn_count + count)

    def assert_stacked_turn(
        self,
        *,
        stacked_turn,
        turn,
        player,
        game,
        card,
        perform_simple_actions=False,
    ):
        self.assertEqual(stacked_turn.turn, turn)
        self.assertEqual(stacked_turn.player, player)
        self.assertEqual(stacked_turn.game, game)
        self.assertEqual(stacked_turn.card, card)
        self.assertEqual(stacked_turn.perform_simple_actions, perform_simple_actions)

    def assert_adhoc_turn_created(self, count=1):
        before_turn_count = AdHocTurn.objects.count()
        yield
        after_turn_count = AdHocTurn.objects.count()
        self.assertEqual(after_turn_count, before_turn_count + count)

    def assert_adhoc_turn(self, *, adhoc_turn, turn, player, game, card):
        self.assertEqual(adhoc_turn.turn, turn)
        self.assertEqual(adhoc_turn.player, player)
        self.assertEqual(adhoc_turn.game, game)
        self.assertEqual(adhoc_turn.card, card)

    def build_card_form(self, adhoc_turn, **kwargs):
        return self.card.adhocturn_form(data=kwargs, adhoc_turn=adhoc_turn)

    def list_diff(self, before, after):
        return list((Counter(after) - Counter(before)).elements())

    def assert_cards_type(self, cards, type, expected=True):
        is_type = f'is_{type}'
        for card in get_cards_from_names(cards):
            self.assertEqual(getattr(card, is_type), expected)

    @contextmanager
    def assert_count_increase(self, deck, source, change):
        before = len(getattr(deck, source))
        yield
        after = len(getattr(deck, source))
        self.assertEqual(after - before, change)

    def assert_top_decks(self, deck, cards):
        top_cards = deck.draw_pile[: len(cards)]
        self.assertEqual(top_cards, cards)
