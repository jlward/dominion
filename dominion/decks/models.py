from django.db import models

from dominion.cards.models import CardInstance


class Deck(models.Model):
    game = models.ForeignKey('games.Game')
    player = models.ForeignKey('players.Player')

    def get_starting_cards(self):
        card_pks = list(CardInstance.objects.filter(
            game=self.game,
            card__name='copper',
            deck=None,
        ).values_list(
            'pk',
            flat=True,
        )[:7])
        card_pks += list(CardInstance.objects.filter(
            game=self.game,
            card__name='estate',
            deck=None,
        ).values_list(
            'pk',
            flat=True,
        )[:3])
        CardInstance.objects.filter(
            pk__in=card_pks,
        ).update(
            deck=self,
        )

    def get_deck_size(self):
        return self.cardinstance_set.count()
