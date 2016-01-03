from django.db import models


class Card(models.Model):
    name = models.CharField(max_length=50)
    cost = models.PositiveSmallIntegerField()
    count = models.PositiveSmallIntegerField(default=10)


class Treasure(Card):
    money_value = models.PositiveSmallIntegerField()


class Victory(Card):
    points = models.PositiveSmallIntegerField()
