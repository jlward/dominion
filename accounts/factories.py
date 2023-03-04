import factory
from django.conf import settings


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Faker('email')
    password = factory.PostGenerationMethodCall('set_password', 'pw')

    class Meta:
        model = settings.AUTH_USER_MODEL
