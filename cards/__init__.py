import importlib
import os

from django.conf import settings

from cards.base import Card


def get_all_cards():
    result = dict()
    path = os.path.join(settings.BASE_DIR, 'cards', 'kingdom_cards')
    for file_name in os.listdir(path):
        if not file_name.endswith('.py'):
            continue
        if file_name == '__init__.py':
            continue
        file_name = file_name[:-3]
        module = importlib.__import__('cards.kingdom_cards', fromlist=[file_name])
        module_file = getattr(module, file_name)
        for klass in dir(module_file):
            if klass.startswith('__'):
                continue
            if klass in ['Card', 'CardTypes']:
                continue
            if not klass[0].isupper():
                continue
            Klass = getattr(module_file, klass)
            if not issubclass(Klass, Card):
                continue
            result[klass] = Klass

    return result


def get_available_kingdom_cards():
    return {k: v for k, v in get_all_cards().items() if not v().is_base_card}


def get_card_from_name(card):
    return get_all_cards()[card]()


def get_cards_from_names(cards):
    return list(get_cards_from_names_as_generator(cards))


def get_cards_from_names_as_generator(cards):
    all_cards = get_all_cards()
    for card in cards:
        yield all_cards[card]()
