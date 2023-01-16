import importlib
import os
import uuid

from django.conf import settings
from django.templatetags.static import static

from cards.constants import CardTypes
from turns.models import Turn


class Card:
    extra_buys = 0
    extra_actions = 0
    extra_cards = 0
    extra_treasure = 0
    extra_victory_points = 0
    cards_in_pile = 10

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def plus_buys(self, *args, **kwargs):
        return self.extra_buys

    @property
    def plus_actions(self, *args, **kwargs):
        return self.extra_actions

    @property
    def plus_cards(self, *args, **kwargs):
        return self.extra_cards

    @property
    def plus_treasures(self, *args, **kwargs):
        return self.extra_treasure

    @property
    def plus_victory_points(self, *args, **kwargs):
        return self.extra_victory_points

    @property
    def cost(self):
        # `card_cost` is not set on purpose. We want this to always be explicitly set.
        return self.card_cost

    @property
    def types(self):
        raise NotImplementedError()

    @property
    def is_action(self):
        return CardTypes.Action in self.types

    @property
    def url(self):
        return static(f'images/{self.name}.jpg')

    def perform_specific_action(self, deck, turn):
        pass

    def perform_action(self, deck, turn: Turn):
        deck.draw_cards(self.plus_cards)
        turn.available_actions += self.plus_actions
        turn.available_buys += self.plus_buys
        turn.available_money += self.plus_treasures
        self.perform_specific_action(deck, turn)

    def __str__(self):
        return self.name
