import factory

from dominion.players.models import Player


class PlayerFactory(factory.django.DjangoModelFactory):
    handle = factory.Sequence(lambda n: "Handle %04d" % n)

    class Meta:
        model = Player
