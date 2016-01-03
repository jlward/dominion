from django.apps import AppConfig
from django.db.models.signals import post_migrate

from dominion.cards.models import Treasure


def create_cards(sender, **kwargs):
    try:
        card = Treasure.objects.get(
            name='copper',
        )
    except Treasure.DoesNotExist:
        card = Treasure(
            name='copper',
            cost=0,
            money_value=1,
        )
    else:
        card.cost = 0
        card.money_value = 1
    card.save()


class CardAppConfig(AppConfig):
    name = 'dominion.cards'
    verbose_name = 'Cards'

    def ready(self):
        post_migrate.connect(create_cards, sender=self)
