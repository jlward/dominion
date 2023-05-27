from django.urls import reverse

from games.models import Game
from players.factories import PlayerFactory
from testing import BaseTestCase


class GamesListTestCase(BaseTestCase):
    url = reverse('game_list')

    def test_GET_returns_200(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)


class GameCreateTestCase(BaseTestCase):
    url = reverse('game_create')

    def setUp(self):
        super().setUp()
        self.opponent = PlayerFactory()
        self.kingdom = ['Village']

    @property
    def params(self):
        return dict(
            player=self.opponent.pk,
            kingdom=self.kingdom,
        )

    def test_POST_redirect_to_game(self):
        r = self.client.post(self.url, self.params)
        game = Game.objects.get()
        game_url = reverse('games_play', kwargs=dict(game_id=game.pk))
        self.assertRedirects(r, game_url)

    def test_POST_redirect_to_game_list(self):
        self.kingdom = ['cesdfasda']
        r = self.client.post(self.url, self.params)
        self.assertRedirects(r, reverse('game_list'))


class PlayActionTestCase(BaseTestCase):
    @property
    def url(self):
        return reverse('games_play_action', kwargs=dict(game_id=self.game.pk))

    def setUp(self):
        super().setUp()
        self.game = self.create_game(players=[self.player, PlayerFactory()])
        self.card = 'Village'

    @property
    def params(self):
        return dict(
            card=self.card,
        )

    def test_playing_invalid_card_returns_ok_false(self):
        r = self.client.post(self.url, self.params)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['okay'], False)


class PlayTreasureTestCase(BaseTestCase):
    @property
    def url(self):
        return reverse('games_play_treasure', kwargs=dict(game_id=self.game.pk))

    def setUp(self):
        super().setUp()
        self.game = self.create_game(players=[self.player, PlayerFactory()])
        self.card = 'Copper'

    @property
    def params(self):
        return dict(
            card=self.card,
        )

    def test_POST_returns_okay_is_true(self):
        r = self.client.post(self.url, self.params)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['okay'], True)

    def test_POST_returns_okay_is_false(self):
        self.card = 'Gold'
        r = self.client.post(self.url, self.params)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['okay'], False)


class PlayAllTreasuresTestCase(BaseTestCase):
    @property
    def url(self):
        return reverse('games_play_all_treasures', kwargs=dict(game_id=self.game.pk))

    @property
    def game_url(self):
        return reverse('games_play', kwargs=dict(game_id=self.game.pk))

    def setUp(self):
        super().setUp()
        self.game = self.create_game(players=[self.player, PlayerFactory()])

    @property
    def params(self):
        return dict()

    def test_POST_returns_302(self):
        r = self.client.post(self.url, self.params, HTTP_REFERER=self.game_url)
        self.assertEqual(r.status_code, 302)
        self.assertRedirects(r, self.game_url)


class BuyKingdomCardTestCase(BaseTestCase):
    @property
    def url(self):
        return reverse('games_buy_kingdom_card', kwargs=dict(game_id=self.game.pk))

    def setUp(self):
        super().setUp()
        self.game = self.create_game(players=[self.player, PlayerFactory()])
        self.card = 'Copper'

    @property
    def params(self):
        return dict(
            card=self.card,
        )

    def test_POST_returns_okay_is_true(self):
        r = self.client.post(self.url, self.params)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['okay'], True)

    def test_POST_returns_okay_is_false(self):
        self.card = 'Gold'
        r = self.client.post(self.url, self.params)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['okay'], False)


class GameHashTestCase(BaseTestCase):
    @property
    def url(self):
        return reverse('game_hash', kwargs=dict(game_id=self.game.pk))

    def setUp(self):
        super().setUp()
        self.game = self.create_game(players=[self.player, PlayerFactory()])

    def test_GET_returns_200(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)
