from django.test import TestCase

from dominion.players.models import Player


class PlayerTestCase(TestCase):
    def test_player_is_created(self):
        player = Player.objects.create(
            handle='Ward',
        )
        assert player
