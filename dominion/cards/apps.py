from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_treasure(Treasure, name, fields):
    try:
        card = Treasure.objects.get(
            name=name,
        )
    except Treasure.DoesNotExist:
        card = Treasure(
            name=name,
            cost=fields['cost'],
            money_value=fields['money_value'],
            count=fields['count']
        )
    else:
        card.cost = fields['cost']
        card.money_value = fields['money_value']
        card.count = fields['count']
    card.save()


def create_victories(Victory, name, fields):
    try:
        card = Victory.objects.get(
            name=name,
        )
    except Victory.DoesNotExist:
        card = Victory(
            name=name,
            cost=fields['cost'],
            points=fields['points'],
            count=fields['count']
        )
    else:
        card.cost = fields['cost']
        card.points = fields['points']
        card.count = fields['count']
    card.save()


def create_cards(sender, **kwargs):
    Treasure = sender.get_model('Treasure')
    Victory = sender.get_model('Victory')
    cards = {
        'copper': {
            'cost': 0,
            'money_value': 1,
            'count': 60,
        },
        'silver': {
            'cost': 3,
            'money_value': 2,
            'count': 40,
        },
        'gold': {
            'cost': 6,
            'money_value': 3,
            'count': 30,
        },
    }
    for name, fields in cards.items():
        create_treasure(Treasure, name, fields)

    cards = {
        'estate': {
            'cost': 2,
            'points': 1,
            'count': 12,
        },
        'duchy': {
            'cost': 5,
            'points': 3,
            'count': 12,
        },
        'province': {
            'cost': 8,
            'points': 6,
            'count': 12,
        },
    }
    for name, fields in cards.items():
        create_victories(Victory, name, fields)


class CardAppConfig(AppConfig):
    name = 'dominion.cards'
    verbose_name = 'Cards'

    def ready(self):
        post_migrate.connect(create_cards, sender=self)
