import factory

from games.factories import GameFactory
from players.factories import PlayerFactory


class TurnFactory(factory.django.DjangoModelFactory):
    turn_number = 1
    game = factory.SubFactory(GameFactory)
    player = factory.SubFactory(PlayerFactory)

    class Meta:
        model = 'turns.Turn'
