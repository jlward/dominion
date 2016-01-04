from django.db import models


class Card(models.Model):
    name = models.CharField(max_length=50)
    cost = models.PositiveSmallIntegerField()
    count = models.PositiveSmallIntegerField(default=10)

    def __str__(self):
        return self.name.title()


class Treasure(Card):
    money_value = models.PositiveSmallIntegerField()


class Victory(Card):
    points = models.PositiveSmallIntegerField()


class CardInstanceManager(models.Manager):
    def create_for_card(self, card, game):
        CardInstance.objects.bulk_create(
            CardInstance(
                card=card,
                game=game,
            ) for _ in range(card.count)
        )


class CardInstance(models.Model):
    card = models.ForeignKey('cards.Card')
    game = models.ForeignKey('games.Game')
    deck = models.ForeignKey(
        'decks.Deck',
        blank=True,
        null=True,
    )

    objects = CardInstanceManager()
