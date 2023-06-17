import uuid

from django.apps import apps
from django.db import models

from cards import get_cards_from_names_as_generator
from games.managers import GameManager


class Game(models.Model):
    objects = GameManager()

    players = models.ManyToManyField('players.Player')
    kingdom = models.JSONField(default=list)
    trash_pile = models.JSONField(default=list)
    game_hash = models.UUIDField()
    turn_order = models.JSONField(default=list)
    is_over = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.check_game_over()
        self.game_hash = uuid.uuid4()
        return super().save(*args, **kwargs)

    def create_turn(self, player):
        Turn = apps.get_model('turns', 'Turn')
        return Turn.objects.create(player=player, game=self, turn_number=1)

    def get_players(self, player):
        if player.pk not in self.turn_order:  # pragma: no cover
            raise NotImplementedError()
        order = self.turn_order[:]
        while player.pk != order[0]:
            order.append(order.pop(0))

        return order

    def get_decks(self, exclude):
        decks = self.decks.all()
        decks = decks.exclude(player=exclude)

        return list(decks)

    def gain_card(self, deck, card, destination='discard_pile'):
        destination_pile = getattr(deck, destination)
        if self.kingdom[card.name] == 0:
            return
        destination_pile.insert(0, card.name)
        self.kingdom[card.name] -= 1

    def trash_cards(self, deck, turn, cards):
        deck.trash_cards(cards)
        turn.trash_cards(cards)
        deck.save()
        self.save()

    @property
    def real_kingdom(self):
        kingdom = get_cards_from_names_as_generator(self.kingdom)
        result = {}
        for card in kingdom:
            count = self.kingdom[card.name]
            if card.unlimited:
                count = '∞'
            result[card.name] = dict(card=card, count=count)

        return result

    @property
    def kingdom_options(self):
        for row in self.real_kingdom.values():
            if row['count'] == 0:
                continue
            yield row['card']

    @property
    def real_base_kingdom(self):
        kingdom = self.real_kingdom
        result = [row for row in kingdom.values() if row['card'].is_base_card]
        return result

    @property
    def real_not_base_kingdom(self):
        kingdom = self.real_kingdom
        result = [row for row in kingdom.values() if not row['card'].is_base_card]
        return result

    @property
    def narnias(self):
        result = []
        for deck in self.decks.all():
            result.extend(deck.narnia_pile)
        return result

    @property
    def winner(self):
        if not self.is_over:
            return '-'
        score = -1000
        winner = None
        for deck in self.decks.all():
            if deck.score > score:
                winner = deck.player
                score = deck.score
                # TODO make ties work
        return winner

    def get_current_turn(self):
        if self.is_over:
            return None

        reaction_turns = self.reactionturns.filter(is_current_turn=True).order_by(
            'turn_order',
        )
        if reaction_turns.exists():
            return reaction_turns[0]

        adhocturns = self.adhocturns.filter(is_current_turn=True).order_by(
            'turn_order',
        )
        if adhocturns.exists():
            return adhocturns[0]

        StackedTurn = apps.get_model('turns', 'StackedTurn')
        adhoc_turn = StackedTurn.objects.process_for_game(self)
        if adhoc_turn:
            return adhoc_turn

        return self.turns.get(is_current_turn=True)

    def end_turn(self, turn):
        turn.perform_cleanup()
        players = self.get_players(turn.player)
        Player = apps.get_model('players', 'Player')
        self.create_turn(Player(pk=players[1]))
        self.save()

    def check_game_over(self):
        if self.kingdom['Province'] < 1:
            self.is_over = True
        if len([count for count in self.kingdom.values() if count < 1]) > 2:
            self.is_over = True

    def move_cards_from_narnias_to_player(self, cards, player, destination):
        decks = list(self.decks.all())
        player_deck = list(deck for deck in decks if deck.player == player)[0]
        for card in cards:
            for deck in decks:
                if card.name in deck.narnia_pile:
                    getattr(player_deck, destination).append(
                        deck.narnia_pile.pop(deck.narnia_pile.index(card.name)),
                    )
                    break
        for deck in decks:
            deck.save()

    def trash_narnias(self):
        decks = list(self.decks.all())
        for deck in decks:
            self.trash_pile.extend(deck.narnia_pile)
            deck.narnia_pile = []
            deck.save()
        self.save()
