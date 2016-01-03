from django.db import models


class Card(models.Model):
    name = models.CharField(max_length=50)
    cost = models.PositiveSmallIntegerField()
    money_value = models.PositiveSmallIntegerField()


class Treasure(Card):
    pass
