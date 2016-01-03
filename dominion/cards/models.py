from django.db import models


class Card(models.Model):
    name = models.CharField(max_length=50)
    cost = models.PositiveSmallIntegerField()


class Treasure(Card):
    money_value = models.PositiveSmallIntegerField()


class Victory(Card):
    points = models.PositiveSmallIntegerField()
