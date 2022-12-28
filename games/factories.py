import factory


class GameFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'games.Game'
