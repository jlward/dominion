import factory


class PlayerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'players.Player'
