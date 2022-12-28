from django.apps import apps
from django.db import models

import cards


class GameManager(models.Manager):
    default_kingdom_cards = [
        'Gold',
        'Silver',
        'Copper',
        'Province',
        'Duchy',
        'Estate',
        'Curse',
    ]

    def _build_kingdom(self):
        kingdom_cards = self.default_kingdom_cards + ['Smithy', 'Village']
        kingdom = {}
        all_cards = cards.get_all_cards()
        for card_name in kingdom_cards:
            Card = all_cards[card_name]
            kingdom[Card.__name__] = Card.cards_in_pile
        return kingdom

    def create_game(self, players):
        Deck = apps.get_model('decks', 'Deck')

        kingdom = self._build_kingdom()
        turn_order = [player.pk for player in players]

        game = self.create(
            kingdom=kingdom,
            turn_order=turn_order,
        )
        game.players.set(players)
        for player in players:
            Deck.objects.create_deck(
                game=game,
                player=player,
            )
        game.save()
        return game
