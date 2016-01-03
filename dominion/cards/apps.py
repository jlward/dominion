from django.apps import AppConfig
from django.db.models.signals import post_migrate

from dominion.cards.models import Treasure, Victory


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


def create_victories(name, fields):
    try:
        card = Victory.objects.get(
            name=name,
        )
    except Victory.DoesNotExist:
        card = Victory(
            name=name,
            cost=fields['cost'],
            points=fields['points'],
        )
    else:
        card.cost = fields['cost']
        card.points = fields['points']
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

    cards = {
        'estate': {
            'cost': 2,
            'points': 1,
        },
        'duchy': {
            'cost': 5,
            'points': 3,
        },
        'province': {
            'cost': 8,
            'points': 6,
        },
    }
    for name, fields in cards.items():
        create_victories(name, fields)


class CardAppConfig(AppConfig):
    name = 'dominion.cards'
    verbose_name = 'Cards'

    def ready(self):
        post_migrate.connect(create_cards, sender=self)
