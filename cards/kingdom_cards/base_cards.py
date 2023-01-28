from cards.base import Card
from cards.constants import CardTypes


class Platinum(Card):
    types = [CardTypes.Treasure]
    extra_treasure = 5
    card_cost = 9
    cards_in_pile = 1000
    unlimited = True


class Gold(Card):
    types = [CardTypes.Treasure]
    extra_treasure = 3
    card_cost = 6
    cards_in_pile = 1000
    unlimited = True


class Silver(Card):
    types = [CardTypes.Treasure]
    extra_treasure = 2
    card_cost = 3
    cards_in_pile = 1000
    unlimited = True


class Copper(Card):
    types = [CardTypes.Treasure]
    extra_treasure = 1
    card_cost = 0
    cards_in_pile = 1000
    unlimited = True


class Colony(Card):
    types = [CardTypes.Victory]
    extra_victory_points = 10
    card_cost = 11


class Province(Card):
    types = [CardTypes.Victory]
    extra_victory_points = 6
    card_cost = 8


class Duchy(Card):
    types = [CardTypes.Victory]
    extra_victory_points = 3
    card_cost = 5


class Estate(Card):
    types = [CardTypes.Victory]
    extra_victory_points = 1
    card_cost = 2


class Curse(Card):
    types = [CardTypes.Curse]
    extra_victory_points = -1
    card_cost = 0
