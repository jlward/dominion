import factory

from cards.kingdom_cards.dominion import Chapel
from games.factories import GameFactory
from players.factories import PlayerFactory


class TurnFactory(factory.django.DjangoModelFactory):
    turn_number = 1
    game = factory.SubFactory(GameFactory)
    player = factory.SubFactory(PlayerFactory)

    class Meta:
        model = 'turns.Turn'


class AdHocTurnFactory(factory.django.DjangoModelFactory):
    turn = factory.SubFactory(TurnFactory)
    game = factory.SubFactory(GameFactory)
    player = factory.SubFactory(PlayerFactory)
    card = Chapel()

    class Meta:
        model = 'turns.AdHocTurn'
