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
        module = importlib.import_module('cards.kingdom_cards', '')
        module_file = getattr(module, file_name)
        for klass in dir(module_file):
            if klass.startswith('__'):
                continue
            if klass in ['Card', 'CardTypes']:
                continue
            Klass = getattr(module_file, klass)
            if not issubclass(Klass, Card):
                continue
            result[klass] = Klass

    return result
