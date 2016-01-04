import factory

from dominion.games.models import Game


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Game
