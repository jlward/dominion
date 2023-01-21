import factory

from accounts.factories import UserFactory


class PlayerFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = 'players.Player'
