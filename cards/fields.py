import inspect

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

        return super().pre_save(model_instance, add)
