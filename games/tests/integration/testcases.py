from django.test import Client
from django.urls import reverse

from players.factories import PlayerFactory
from testing import BaseTestCase
from testing.utils import css_select, css_select_get_attributes, css_select_get_text


class IntegrationTestCase(BaseTestCase):
    player_starting_hand = None
    opponent_starting_hand = None

    @property
    def game_url(self):
        return reverse('games_play', kwargs=dict(game_id=self.game.pk))

    @property
    def play_action_url(self):
        return reverse('games_play_action', kwargs=dict(game_id=self.game.pk))

    def setUp(self):
        super().setUp()
        self.player = PlayerFactory()
        self.opponent = PlayerFactory()

        self.game = self.create_game(players=[self.player, self.opponent])

        self.player_deck = self.game.decks.get(player=self.player)
        self.opponent_deck = self.game.decks.get(player=self.opponent)

        if self.player_starting_hand:
            self.player_deck.hand = self.player_starting_hand[:]
            self.player_deck.save()

        if self.opponent_starting_hand:
            self.opponent_deck.hand = self.opponent_starting_hand[:]
            self.opponent_deck.save()

        self.player_client = Client()
        self.opponent_client = Client()

        self.player_client.force_login(self.player.user)
        self.opponent_client.force_login(self.opponent.user)

    def assert_initial_state(self):
        r = self.player_client.get(self.game_url)
        self.assert_your_turn(r)
        self.assertEqual(self.get_resources(r), dict(actions=1, buys=1, money=0))
        if self.player_starting_hand:
            self.assertEqual(self.get_player_hand(r), self.player_starting_hand)

        r = self.opponent_client.get(self.game_url)
        self.assert_not_your_turn(r)
        self.assertEqual(
            self.get_resources(r),
            dict(actions=None, buys=None, money=None),
        )
        if self.opponent_starting_hand:
            self.assertEqual(self.get_oppnent_hand(r), self.opponent_starting_hand)

    def assert_your_turn(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(
            css_select_get_text(response, '.state'),
            ['Waiting'],
        )

    def assert_not_your_turn(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            css_select_get_text(response, '.state'),
            ['Waiting'],
        )

    def _get_actions(self, response):
        return css_select_get_text(response, '#actions span')[0][1:-1]

    def _get_buys(self, response):
        return css_select_get_text(response, '#buys span')[0][1:-1]

    def _get_money(self, response):
        return css_select_get_text(response, '#money span')[0][1:-1]

    def get_resources(self, response):
        try:
            actions = int(self._get_actions(response))
        except IndexError:
            actions = None
        try:
            buys = int(self._get_buys(response))
        except IndexError:
            buys = None
        try:
            money = int(self._get_money(response))
        except IndexError:
            money = None
        return dict(
            actions=actions,
            buys=buys,
            money=money,
        )

    def get_player_hand(self, response):
        r = self.player_client.get(self.game_url)
        hand = css_select_get_attributes(r, '#hand .card.in_hand', ['data-name'])
        return [row['data-name'] for row in hand]

    def get_oppnent_hand(self, response):
        r = self.opponent_client.get(self.game_url)
        hand = css_select_get_attributes(r, '#hand .card.in_hand', ['data-name'])
        return [row['data-name'] for row in hand]

    def player_play_card(self, card):
        r = self.player_client.post(self.play_action_url, dict(card=card), follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['okay'], True)

    def opponent_play_card(self, card):
        raise NotImplementedError()

    def assert_player_adhoc_turn_modal_present(self):
        r = self.player_client.get(self.game_url)
        assert css_select(r, '#adhocturnModal')

    def assert_player_adhoc_turn_modal_not_present(self):
        r = self.player_client.get(self.game_url)
        assert not css_select(r, '#adhocturnModal')

    def assert_opponent_adhoc_turn_modal_present(self):
        r = self.opponent_client.get(self.game_url)
        assert css_select(r, '#adhocturnModal')

    def assert_opponent_adhoc_turn_modal_not_present(self):
        r = self.opponent_client.get(self.game_url)
        assert not css_select(r, '#adhocturnModal')

    def player_pick_cards_from_modal(self, *cards):
        r = self.player_client.get(self.game_url)
        form_actions = css_select_get_attributes(r, '#adhocturnModal form', ['action'])
        url = form_actions[0]['action']

        r = self.player_client.post(url, dict(cards=cards), HTTP_REFERER=self.game_url)
        self.assertEqual(r.status_code, 302)
        self.assertRedirects(r, self.game_url)

    def oppenent_pick_cards_from_modal(self, *cards):
        r = self.opponent_client.get(self.game_url)
        form_actions = css_select_get_attributes(r, '#adhocturnModal form', ['action'])
        url = form_actions[0]['action']

        r = self.opponent_client.post(
            url,
            dict(cards=cards),
            HTTP_REFERER=self.game_url,
        )
        self.assertEqual(r.status_code, 302)
        self.assertRedirects(r, self.game_url)
