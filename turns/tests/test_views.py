from unittest import mock

from django.urls import reverse

from testing import BaseTestCase
from turns.factories import AdHocTurnFactory, TurnFactory


class EndPhaseTestCase(BaseTestCase):
    @property
    def url(self):
        return reverse('turns_end_phase', kwargs=dict(turn_id=self.turn.pk))

    redirect_url = reverse('accounts_login')

    def setUp(self):
        super().setUp()
        self.turn = TurnFactory()

    def test_turn_state_action(self):
        game_hash = self.turn.game.game_hash
        self.turn.state = 'action'
        self.turn.save()

        r = self.client.post(self.url, HTTP_REFERER=self.redirect_url)
        self.assertEqual(r.status_code, 302)

        self.turn.refresh_from_db()
        self.assertEqual(self.turn.state, 'buy')

        self.assertNotEqual(self.turn.game.game_hash, game_hash)

    def test_turn_state_buy(self):
        game_hash = self.turn.game.game_hash
        self.turn.state = 'buy'
        self.turn.save()

        with mock.patch('games.models.Game.end_turn'):
            r = self.client.post(self.url, HTTP_REFERER=self.redirect_url)

        self.assertEqual(r.status_code, 302)

        self.turn.refresh_from_db()
        self.assertEqual(self.turn.state, 'end')

        self.assertNotEqual(self.turn.game.game_hash, game_hash)

    def test_turn_state_unknown(self):
        game_hash = self.turn.game.game_hash
        self.turn.state = 'foo'
        self.turn.save()

        r = self.client.post(self.url, HTTP_REFERER=self.redirect_url)
        self.assertEqual(r.status_code, 302)

        self.turn.refresh_from_db()
        self.assertEqual(self.turn.state, 'foo')

        self.assertNotEqual(self.turn.game.game_hash, game_hash)


class PerformActionTestCase(BaseTestCase):
    @property
    def url(self):
        return reverse(
            'turns_adhocturn_perform_action',
            kwargs=dict(turn_id=self.turn.pk),
        )

    redirect_url = reverse('accounts_login')

    def setUp(self):
        super().setUp()
        self.game = self.create_game()
        self.current_turn = self.game.get_current_turn()
        self.turn = AdHocTurnFactory(
            game=self.game,
            turn=self.current_turn,
            player=self.current_turn.player,
        )

    def test_form_valid(self):
        game_hash = self.game.game_hash
        r = self.client.post(self.url, HTTP_REFERER=self.redirect_url)
        self.assertEqual(r.status_code, 302)
        self.turn.refresh_from_db()
        self.assertEqual(self.turn.is_current_turn, False)
        self.game.refresh_from_db()
        self.assertNotEqual(self.game.game_hash, game_hash)

    def test_form_invalid(self):
        game_hash = self.game.game_hash

        with mock.patch('cards.forms.dominion.ChapelForm.is_valid', return_value=False):
            r = self.client.post(self.url, HTTP_REFERER=self.redirect_url)
        self.assertEqual(r.status_code, 302)
        self.turn.refresh_from_db()
        self.assertEqual(self.turn.is_current_turn, True)
        self.game.refresh_from_db()
        self.assertEqual(self.game.game_hash, game_hash)
