from django.test import TestCase


class SmokeTestCase(TestCase):
    def test_wsgi(self):
        import dominion.wsgi
        assert dominion.wsgi

    def test_url(self):
        import dominion.urls
        assert dominion.urls
