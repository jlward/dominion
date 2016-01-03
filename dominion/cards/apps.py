from django.apps import AppConfig
from django.db.models.signals import post_migrate

from dominion.cards.models import Treasure


def create_treasure(name, fields):
    try:
        card = Treasure.objects.get(
            name=name,
        )
    except Treasure.DoesNotExist:
        card = Treasure(
            name=name,
            cost=fields['cost'],
            money_value=fields['money_value'],
        )
    else:
        card.cost = fields['cost']
        card.money_value = fields['money_value']
    card.save()


def create_cards(sender, **kwargs):
    cards = {
        'copper': {
            'cost': 0,
            'money_value': 1,
        },
        'silver': {
            'cost': 3,
            'money_value': 2,
        },
        'gold': {
            'cost': 6,
            'money_value': 3,
        },
    }
    for name, fields in cards.items():
        create_treasure(name, fields)


class CardAppConfig(AppConfig):
    name = 'dominion.cards'
    verbose_name = 'Cards'

    def ready(self):
        post_migrate.connect(create_cards, sender=self)
