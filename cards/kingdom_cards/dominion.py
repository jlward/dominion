from cards.base import Card
from cards.constants import CardTypes
from cards.kingdom_cards.base_cards import Curse


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
