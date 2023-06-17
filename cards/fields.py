import inspect
import json

from django.db import models


class CardField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 100
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        from cards import get_all_cards

        cards = get_all_cards()
        return cards[value]()

    def pre_save(self, model_instance, add: bool):
        from cards.base import Card

        if inspect.isclass(model_instance.card):
            if issubclass(model_instance.card, Card):
                model_instance.card = model_instance.card.__name__
            else:
                raise TypeError(f'{model_instance.card} is not a valid Card')

        return super().pre_save(model_instance, add)


class CardsField(models.TextField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('default', [])
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        from cards import get_cards_from_names

        return get_cards_from_names(json.loads(value))

    def get_prep_value(self, value):
        return json.dumps(
            [card if isinstance(card, str) else card.name for card in value],
        )
