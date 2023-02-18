from cards.base import Card
from cards.constants import CardTypes
from cards.forms.dominion import (
    CellarForm,
    ChapelForm,
    FeastForm,
    MoneylenderForm,
    WorkshopForm,
)
from cards.kingdom_cards.base_cards import Curse
from turns.models import AdHocTurn


class CouncilRoom(Card):
    types = [CardTypes.Action]
    card_cost = 5
    extra_cards = 4
    extra_buys = 1

    def perform_specific_action(self, deck, turn):
        game = turn.game
        players = game.get_players(turn.player)
        # remove current player from list
        players.pop(0)
        for player_id in players:
            deck = game.decks.get(player_id=player_id)
            deck.draw_cards(1)
            deck.save()


class Festival(Card):
    types = [CardTypes.Action]
    card_cost = 5
    extra_actions = 2
    extra_buys = 1
    extra_treasure = 2


class Laboratory(Card):
    types = [CardTypes.Action]
    card_cost = 5
    extra_cards = 2
    extra_actions = 1


class Market(Card):
    types = [CardTypes.Action]
    card_cost = 5
    extra_cards = 1
    extra_actions = 1
    extra_buys = 1
    extra_treasure = 1


class Smithy(Card):
    types = [CardTypes.Action]
    card_cost = 4
    extra_cards = 3


class Village(Card):
    types = [CardTypes.Action]
    card_cost = 3
    extra_cards = 1
    extra_actions = 2


class Witch(Card):
    types = [CardTypes.Action, CardTypes.Attack]
    card_cost = 5
    extra_cards = 2

    def perform_specific_action(self, deck, turn):
        game = turn.game
        players = game.get_players(turn.player)
        # remove current player from list
        players.pop(0)
        for player_id in players:
            deck = game.decks.get(player_id=player_id)
            game.gain_card(deck, Curse())
            deck.save()
        game.save()


class Woodcutter(Card):
    types = [CardTypes.Action]
    card_cost = 3
    extra_buys = 1
    extra_treasure = 2


class Chapel(Card):
    types = [CardTypes.Action]
    card_cost = 2
    adhocturn_action_title = 'Select up to 4 cards to trash'
    adhocturn_form = ChapelForm

    def perform_specific_action(self, deck, turn):
        AdHocTurn.objects.create(
            turn=turn,
            player=turn.player,
            game=turn.game,
            card=self,
        )


# class Adventurer(Card):
#     pass


# class Bureaucrat(Card):
#     pass


class Cellar(Card):
    types = [CardTypes.Action]
    card_cost = 2
    extra_actions = 1
    adhocturn_action_title = 'Select cards to discard'
    adhocturn_form = CellarForm

    def perform_specific_action(self, deck, turn):
        AdHocTurn.objects.create(
            turn=turn,
            player=turn.player,
            game=turn.game,
            card=self,
        )


# class Chancellor(Card):
#     pass


class Feast(Card):
    types = [CardTypes.Action]
    card_cost = 4
    adhocturn_action_title = 'Gain a card costing up to 5'
    adhocturn_form = FeastForm

    def perform_specific_action(self, deck, turn):
        deck.trash_cards(cards=[Feast()], source='played_cards')
        AdHocTurn.objects.create(
            turn=turn,
            player=turn.player,
            game=turn.game,
            card=self,
        )


# class Gardens(Card):
#     pass


# class Library(Card):
#     pass


# class Militia(Card):
#     pass


# class Mine(Card):
#     pass


# class Moat(Card):
#     pass


class Moneylender(Card):
    types = [CardTypes.Action]
    card_cost = 4
    adhocturn_action_title = 'Trash a Copper?'
    adhocturn_form = MoneylenderForm

    def perform_specific_action(self, deck, turn):
        if 'Copper' not in deck.hand:
            return
        AdHocTurn.objects.create(
            turn=turn,
            player=turn.player,
            game=turn.game,
            card=self,
        )


# class Remodel(Card):
#     pass


# class Spy(Card):
#     pass


# class Thief(Card):
#     pass


# class ThroneRoom(Card):
#     pass


class Workshop(Card):
    types = [CardTypes.Action]
    card_cost = 3
    adhocturn_action_title = 'Gain a card costing up to 4'
    adhocturn_form = WorkshopForm

    def perform_specific_action(self, deck, turn):
        AdHocTurn.objects.create(
            turn=turn,
            player=turn.player,
            game=turn.game,
            card=self,
        )
