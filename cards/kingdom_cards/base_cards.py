from cards.base import Card


class Platinum(Card):
    extra_treasure = 5
    card_cost = 9


class Gold(Card):
    extra_treasure = 3
    card_cost = 6


class Silver(Card):
    extra_treasure = 2
    card_cost = 3


class Copper(Card):
    extra_treasure = 1
    card_cost = 0


class Colony(Card):
    extra_victory_points = 10
    card_cost = 11


class Province(Card):
    extra_victory_points = 6
    card_cost = 8


class Duchy(Card):
    extra_victory_points = 3
    card_cost = 5


class Estate(Card):
    extra_victory_points = 1
    card_cost = 2


class Curse(Card):
    extra_victory_points = -1
    card_cost = 0
