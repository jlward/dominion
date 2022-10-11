import importlib
import os
import uuid

from django.conf import settings


def noop():
    return 0


class Card:
    def __init__(self, *, name, _id=None):
        self.name = name
        self.validate_name()
        # This is to keep track of unique versions of duration cards.
        if not _id:
            _id = uuid.uuid4()
        self.id = _id

    @property
    def card_repo(self):
        return os.path.join(
            settings.BASE_DIR,
            'cards',
            'card_repo',
            self.name,
        )

    def validate_name(self):
        # Check to make sure that self.name is in our dataset.
        if not os.path.exists(self.card_repo):
            raise ValueError(f'"{self.name}" is not a valid card')

    def process_card(self, game):
        # Placeholder for shitty cards like shanty town and stonemasons
        pass

    def get_modifier_function(self, name, fail_silently=True):
        try:
            module = importlib.import_module(f'cards.card_repo.{self.name}.{name}')
        except ModuleNotFoundError:
            if fail_silently:
                return noop
            raise ValueError(f'"{self.name}" is missing {name}')
        return getattr(module, name)

    @property
    def plus_buys(self, *args, **kwargs):
        return self.get_modifier_function('buys')()

    @property
    def plus_actions(self, *args, **kwargs):
        return self.get_modifier_function('actions')()

    @property
    def plus_cards(self, *args, **kwargs):
        return self.get_modifier_function('cards')()

    @property
    def plus_treasures(self, *args, **kwargs):
        return self.get_modifier_function('treasures')()

    @property
    def plus_victory_points(self, *args, **kwargs):
        return self.get_modifier_function('victory_points')()

    @property
    def cost(self):
        func = self.get_modifier_function('cost', fail_silently=False)
        return func()
