from django.urls import reverse

from accounts.factories import UserFactory
from testing import BaseTestCase


class LoginTestCase(BaseTestCase):
    url = reverse('accounts_login')
    auto_login_player = False

    def setUp(self):
        super().setUp()
        self.email = self.faker.email()
        self.password = self.faker.password()
        self.user = UserFactory(email=self.email, password=self.password)

    @property
    def params(self):
        return dict(email=self.email, password=self.password)

    def test_user_logged_in(self):
        r = self.client.post(self.url, self.params)
        self.assertEqual(r.status_code, 302)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.user.pk)

    def test_GET_returns_200(self):
        r = self.client.get(self.url)
        self.assertEqual(r.status_code, 200)

    def test_POST_returns_200_password_wrong(self):
        self.password = 'foo'
        r = self.client.post(self.url, self.params)
        self.assertEqual(r.status_code, 200)

    def test_POST_returns_200_form_invalid(self):
        self.email = ''
        self.password = ''
        r = self.client.post(self.url, self.params)
        self.assertEqual(r.status_code, 200)
