import factory

from games.factories import GameFactory
from players.factories import PlayerFactory


class DeckFactory(factory.django.DjangoModelFactory):
    hand = factory.Sequence(
        lambda n: ['Copper', 'Copper', 'Silver', 'Village', 'Estate'],
    )
    draw_pile = factory.Sequence(lambda n: ['Smithy', 'Copper', 'Silver'])
    discard_pile = factory.Sequence(lambda n: ['Gold', 'Province'])
    game = factory.SubFactory(GameFactory)
    player = factory.SubFactory(PlayerFactory)

    class Meta:
        model = 'decks.Deck'
