from cards import get_card_from_name
from cards.base import Card
from cards.constants import CardTypes
from cards.forms.dominion import (
    CellarForm,
    ChapelForm,
    FeastForm,
    MineForm,
    MoneylenderForm,
    RemodelForm,
    SpyForm,
    ThroneRoomForm,
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


class Adventurer(Card):
    types = [CardTypes.Action]
    card_cost = 6

    def perform_specific_action(self, deck, turn):
        revealed_cards = []
        revealed_treasures = []

        while len(revealed_treasures) < 2:
            top_deck = deck.top_deck()
            if top_deck is None:
                break
            card = get_card_from_name(top_deck)
            if card.is_treasure:
                revealed_treasures.append(card.name)
            else:
                revealed_cards.append(card.name)

        deck.hand.extend(revealed_treasures)
        deck.discard_pile.extend(revealed_cards)
        deck.save()


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


class Gardens(Card):
    types = [CardTypes.Victory]
    card_cost = 4

    def get_victory_points(self, deck, *args, **kwargs):
        num_cards = len(deck.all_cards)
        return num_cards // 10


# class Library(Card):
#     pass


# class Militia(Card):
#     pass


class Mine(Card):
    types = [CardTypes.Action]
    card_cost = 5
    adhocturn_action_title = 'Trash a treasure? - Gain a treasure costing up to 3 more'
    adhocturn_form = MineForm

    def perform_specific_action(self, deck, turn):
        AdHocTurn.objects.create(
            turn=turn,
            player=turn.player,
            game=turn.game,
            card=self,
        )


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


class Remodel(Card):
    types = [CardTypes.Action]
    card_cost = 4
    adhocturn_action_title = 'Trash a card? - Gain a card costing up to 2 more'
    adhocturn_form = RemodelForm

    def perform_specific_action(self, deck, turn):
        AdHocTurn.objects.create(
            turn=turn,
            player=turn.player,
            game=turn.game,
            card=self,
        )


class Spy(Card):
    types = [CardTypes.Action, CardTypes.Attack]
    card_cost = 4
    extra_actions = 1
    extra_cards = 1
    adhocturn_action_title = 'Discard?'
    adhocturn_form = SpyForm

    def perform_specific_action(self, deck, turn):
        for player in deck.game.players.all():
            player_deck = player.decks.get(game=deck.game)
            if len(player_deck.draw_pile) < 1:
                player_deck.full_shuffle()
                player_deck.save()
                if len(player_deck.draw_pile) < 1:
                    continue
            AdHocTurn.objects.create(
                turn=turn,
                player=turn.player,
                game=turn.game,
                card=self,
                target_player=player,
            )


# class Thief(Card):
#     pass


class ThroneRoom(Card):
    types = [CardTypes.Action]
    card_cost = 4
    adhocturn_action_title = 'Pick an action to play twice'
    adhocturn_form = ThroneRoomForm

    def perform_specific_action(self, deck, turn):
        AdHocTurn.objects.create(
            turn=turn,
            player=turn.player,
            game=turn.game,
            card=self,
        )


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
