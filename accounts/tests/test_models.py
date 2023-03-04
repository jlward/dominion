from accounts.models import User
from testing import BaseTestCase


class ManagerCreateUserTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.email = self.faker.email()
        self.password = self.faker.password()

    def test_create_user(self):
        user = User.objects.create_user(email=self.email)
        user.refresh_from_db()
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.is_staff, False)
        self.assertEqual(user.is_superuser, False)
        self.assertEqual(user.has_usable_password(), False)

    def test_create_user_requires_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None)

    def test_create_superuser(self):
        user = User.objects.create_superuser(email=self.email, password=self.password)
        user.refresh_from_db()
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.check_password(self.password), True)
        self.assertEqual(user.is_staff, True)
        self.assertEqual(user.is_superuser, True)

    def test_superuser_is_not_staff(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=self.email,
                password=self.password,
                is_staff=False,
            )

    def test_superuser_is_not_superuser(self):
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email=self.email,
                password=self.password,
                is_superuser=False,
            )
