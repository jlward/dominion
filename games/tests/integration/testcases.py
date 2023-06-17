from django.test import Client
from django.urls import reverse

from players.factories import PlayerFactory
from testing import BaseTestCase
from testing.utils import css_select, css_select_get_attributes, css_select_get_text


class IntegrationTestCase(BaseTestCase):
    player_starting_hand = None
    player_starting_draw_pile = None
    player_starting_discard_pile = None
    opponent_starting_hand = None
    opponent_starting_draw_pile = None
    opponent_starting_discard_pile = None

    @property
    def game_url(self):
        return reverse('games_play', kwargs=dict(game_id=self.game.pk))

    @property
    def play_action_url(self):
        return reverse('games_play_action', kwargs=dict(game_id=self.game.pk))

    def setUp(self):
        super().setUp()
        self.player = PlayerFactory(handle='player')
        self.opponent = PlayerFactory(handle='opponent')

        self.game = self.create_game(players=[self.player, self.opponent])

        self.player_deck = self.game.decks.get(player=self.player)
        self.opponent_deck = self.game.decks.get(player=self.opponent)

        if self.player_starting_hand is not None:
            self.player_deck.hand = self.player_starting_hand[:]
        if self.opponent_starting_hand is not None:
            self.opponent_deck.hand = self.opponent_starting_hand[:]

        if self.player_starting_draw_pile is not None:
            self.player_deck.draw_pile = self.player_starting_draw_pile[:]
        if self.opponent_starting_draw_pile is not None:
            self.opponent_deck.draw_pile = self.opponent_starting_draw_pile[:]

        if self.player_starting_discard_pile is not None:
            self.player_deck.discard_pile = self.player_starting_discard_pile
        if self.opponent_starting_discard_pile is not None:
            self.opponent_deck.discard_pile = self.opponent_starting_discard_pile

        self.player_deck.save()
        self.opponent_deck.save()

        self.player_client = Client()
        self.opponent_client = Client()

        self.player_client.force_login(self.player.user)
        self.opponent_client.force_login(self.opponent.user)

        self.player.client = self.player_client
        self.opponent.client = self.opponent_client
        self.player_client.player = self.player
        self.opponent_client.player = self.opponent

        del self.client
        self.assert_initial_state()

    def assert_initial_state(self):
        self.assert_player_turn(self.player, True)

        self.assert_resources_for_player(self.player)

        if self.player_starting_hand:
            self.assert_hand(self.player, self.player_starting_hand)

        self.assert_player_turn(self.opponent, False)
        self.assert_resources_for_player(
            self.opponent,
            actions=None,
            buys=None,
            money=None,
        )
        if self.opponent_starting_hand:
            self.assert_hand(self.opponent, self.opponent_starting_hand)

    def assert_player_turn(self, player, yes_or_no):
        r = player.client.get(self.game_url)
        self.assertEqual(r.status_code, 200)
        if yes_or_no:
            self.assertNotEqual(
                css_select_get_text(r, '.state'),
                ['Waiting'],
            )
        else:
            self.assertEqual(
                css_select_get_text(r, '.state'),
                ['Waiting'],
            )

    def _get_actions(self, response):
        return css_select_get_text(response, '#actions span')[0][1:-1]

    def _get_buys(self, response):
        return css_select_get_text(response, '#buys span')[0][1:-1]

    def _get_money(self, response):
        return css_select_get_text(response, '#money span')[0][1:-1]

    def _get_resources(self, response):
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

    def assert_resources_for_player(self, player, actions=1, buys=1, money=0):
        r = player.client.get(self.game_url)
        resources = self._get_resources(r)
        self.assertEqual(resources['actions'], actions)
        self.assertEqual(resources['buys'], buys)
        self.assertEqual(resources['money'], money)

    def get_hand(self, player):
        r = player.client.get(self.game_url)
        hand = css_select_get_attributes(r, '#hand .card.in_hand', ['data-name'])
        hand = [row['data-name'] for row in hand]
        return hand

    def assert_hand(self, player, expected_hand):
        hand = self.get_hand(player)
        self.assertCountEqual(hand, expected_hand)

    def assert_hand_size(self, player, expected_count):
        self.assertEqual(len(self.get_hand(player)), expected_count)

    def play_card(self, player, card):
        r = player.client.post(self.play_action_url, dict(card=card), follow=True)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['okay'], True)

    def assert_adhoc_model_for_player(self, player, present):
        r = player.client.get(self.game_url)
        if present:
            assert css_select(
                r,
                '#adhocturnModal',
            ), 'Player should see adhoc modal and is not'
        else:
            assert not css_select(
                r,
                '#adhocturnModal',
            ), 'Player should not see adhoc modal and is'

    def pick_yes_no_from_modal(self, player, answer):
        r = player.client.get(self.game_url)
        form_actions = css_select_get_attributes(r, '#adhocturnModal form', ['action'])
        url = form_actions[0]['action']

        r = player.client.post(
            url,
            dict(selection=answer),
            HTTP_REFERER=self.game_url,
        )
        self.assertEqual(r.status_code, 302)
        self.assertRedirects(r, self.game_url)

    def pick_cards_from_modal(self, player, *cards, **extra_params):
        r = player.client.get(self.game_url)
        form_actions = css_select_get_attributes(r, '#adhocturnModal form', ['action'])
        url = form_actions[0]['action']

        params = dict(cards=cards)
        params.update(extra_params)
        r = player.client.post(
            url,
            params,
            HTTP_REFERER=self.game_url,
        )
        self.assertEqual(r.status_code, 302)
        self.assertRedirects(r, self.game_url)

    def assert_card_in_discard(self, player, card):
        r = player.client.get(self.game_url)
        discard_pile = css_select_get_attributes(
            r,
            '#discard-modal .modal-body .card',
            ['data-name'],
        )
        discard = [row['data-name'] for row in discard_pile]
        assert card in discard
