import factory


def starting_kingdom(n):
    return dict(
        Gold=1000,
        Silver=1000,
        Copper=986,
        # This is wrong for two players
        Province=10,
        # This is wrong for two players
        Duchy=10,
        # This is wrong for two players
        Estate=10,
        Curse=10,
        Smithy=10,
        Village=10,
    )


class GameFactory(factory.django.DjangoModelFactory):
    kingdom = factory.Sequence(starting_kingdom)

    class Meta:
        model = 'games.Game'
