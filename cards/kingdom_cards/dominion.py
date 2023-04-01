from cards import get_card_from_name
from cards.base import Card
from cards.constants import CardTypes
from cards.forms.dominion import (
    BureaucratForm,
    CellarForm,
    ChancellorForm,
    ChapelForm,
    FeastForm,
    MilitiaForm,
    MineForm,
    MoneylenderForm,
    RemodelForm,
    SpyForm,
    ThroneRoomForm,
    WorkshopForm,
)
from cards.kingdom_cards.base_cards import Curse, Silver
from turns.models import QueuedTurn


class Adventurer(Card):
    types = [CardTypes.Action]
    card_cost = 6

    def perform_specific_action(self, deck):
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


class Bureaucrat(Card):
    types = [CardTypes.Action, CardTypes.Attack]
    card_cost = 4
    adhocturn_action_title = 'Reveal a Victory Card to put on top of your deck'
    adhocturn_form = BureaucratForm

    def perform_specific_action(self, deck, turn):
        queued_turns = []
        for player in deck.game.players.all():
            if player.pk == turn.player_id:
                continue
            queued_turns.append(
                QueuedTurn.objects.create(
                    turn=turn,
                    player=player,
                    game=turn.game,
                    card=self,
                ),
            )
        return queued_turns

    def perform_specific_queued_action(self, queued_turn):
        super().perform_specific_queued_action(queued_turn)
        # TODO stop doing this. add deck to turns
        deck = queued_turn.game.decks.get(player=queued_turn.player)
        deck.game.gain_card(deck, Silver(), destination='draw_pile')
        deck.save()

    def should_create_adhoc_turn(self, queued_turn):
        player_deck = queued_turn.player.decks.get(game=queued_turn.game)
        v_in_hand = list(card for card in player_deck.real_hand if card.is_victory)
        if not v_in_hand:
            return False
        if len(v_in_hand) > 1:
            return True
        player_deck.move_to_top_deck(v_in_hand[0])
        player_deck.save()
        return False


class Cellar(Card):
    types = [CardTypes.Action]
    card_cost = 2
    extra_actions = 1
    adhocturn_action_title = 'Select cards to discard'
    adhocturn_form = CellarForm

    def perform_specific_action(self, deck, turn):
        queued_turns = []
        queued_turns.append(
            QueuedTurn.objects.create(
                turn=turn,
                player=turn.player,
                game=turn.game,
                card=self,
            ),
        )
        queued_turns.append(
            QueuedTurn.objects.create(
                turn=turn,
                player=turn.player,
                game=turn.game,
                card=self,
                perform_simple_actions=True,
            ),
        )
        return queued_turns

    def should_create_adhoc_turn(self, queued_turn):
        deck = queued_turn.game.decks.get(player=queued_turn.player)
        if not deck.hand:
            return False
        return True


class Chancellor(Card):
    types = [CardTypes.Action]
    card_cost = 3
    extra_treasure = 2
    adhocturn_action_title = 'Put deck in discard?'
    adhocturn_form = ChancellorForm

    def perform_specific_action(self, deck, turn):
        queued_turns = []
        queued_turns.append(
            QueuedTurn.objects.create(
                turn=turn,
                player=turn.player,
                game=turn.game,
                card=self,
            ),
        )
        queued_turns.append(
            QueuedTurn.objects.create(
                turn=turn,
                player=turn.player,
                game=turn.game,
                card=self,
                perform_simple_actions=True,
            ),
        )
        return queued_turns

    def should_create_adhoc_turn(self, queued_turn):
        deck = queued_turn.game.decks.get(player=queued_turn.player)
        if not deck.draw_pile:
            return False
        return True


class Chapel(Card):
    types = [CardTypes.Action]
    card_cost = 2
    adhocturn_action_title = 'Select up to 4 cards to trash'
    adhocturn_form = ChapelForm

    def perform_specific_action(self, deck, turn):
        return QueuedTurn.objects.create(
            turn=turn,
            player=turn.player,
            game=turn.game,
            card=self,
        )

    def should_create_adhoc_turn(self, queued_turn):
        deck = queued_turn.game.decks.get(player=queued_turn.player)
        if not deck.hand:
            return False
        return True


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


class Feast(Card):
    types = [CardTypes.Action]
    card_cost = 4
    adhocturn_action_title = 'Gain a card costing up to 5'
    adhocturn_form = FeastForm

    def perform_specific_action(self, deck, turn):
        return QueuedTurn.objects.create(
            turn=turn,
            player=turn.player,
            game=turn.game,
            card=self,
        )

    def perform_specific_queued_action(self, queued_turn):
        super().perform_specific_queued_action(queued_turn)
        # TODO stop doing this. add deck to turns
        deck = queued_turn.game.decks.get(player=queued_turn.player)
        deck.trash_cards(cards=[Feast()], source='played_cards')

    def should_create_adhoc_turn(self, queued_turn):
        return True


class Festival(Card):
    types = [CardTypes.Action]
    card_cost = 5
    extra_actions = 2
    extra_buys = 1
    extra_treasure = 2


class Gardens(Card):
    types = [CardTypes.Victory]
    card_cost = 4

    def get_victory_points(self, deck, *args, **kwargs):
        num_cards = len(deck.all_cards)
        return num_cards // 10


class Laboratory(Card):
    types = [CardTypes.Action]
    card_cost = 5
    extra_cards = 2
    extra_actions = 1


# class Library(Card):
#     pass


class Market(Card):
    types = [CardTypes.Action]
    card_cost = 5
    extra_cards = 1
    extra_actions = 1
    extra_buys = 1
    extra_treasure = 1


class Militia(Card):
    types = [CardTypes.Action, CardTypes.Attack]
    card_cost = 4
    extra_treasure = 2
    # TODO fix title for less than 3 cards in hand
    adhocturn_action_title = 'Pick 3 cards to keep'
    adhocturn_form = MilitiaForm

    def perform_specific_action(self, deck, turn):
        queued_turns = []
        for player in deck.game.players.all():
            if player.pk == turn.player_id:
                continue
            queued_turns.append(
                QueuedTurn.objects.create(
                    turn=turn,
                    player=player,
                    game=turn.game,
                    card=self,
                ),
            )
        queued_turns.append(
            QueuedTurn.objects.create(
                turn=turn,
                player=turn.player,
                game=turn.game,
                card=self,
                perform_simple_actions=True,
            ),
        )
        return queued_turns

    def should_create_adhoc_turn(self, queued_turn):
        player_deck = queued_turn.player.decks.get(game=queued_turn.game)
        if len(player_deck.hand) < 4:
            return False
        return True


class Mine(Card):
    types = [CardTypes.Action]
    card_cost = 5
    adhocturn_action_title = 'Trash a treasure? - Gain a treasure costing up to 3 more'
    adhocturn_form = MineForm

    def perform_specific_action(self, deck, turn):
        return QueuedTurn.objects.create(
            turn=turn,
            player=turn.player,
            game=turn.game,
            card=self,
        )

    def should_create_adhoc_turn(self, queued_turn):
        player_deck = queued_turn.player.decks.get(game=queued_turn.game)
        if player_deck.no_treasure:
            return False
        return True


# class Moat(Card):
#     pass


class Moneylender(Card):
    types = [CardTypes.Action]
    card_cost = 4
    adhocturn_action_title = 'Trash a Copper?'
    adhocturn_form = MoneylenderForm

    def perform_specific_action(self, deck, turn):
        return QueuedTurn.objects.create(
            turn=turn,
            player=turn.player,
            game=turn.game,
            card=self,
        )

    def should_create_adhoc_turn(self, queued_turn):
        player_deck = queued_turn.player.decks.get(game=queued_turn.game)
        if 'Copper' not in player_deck.hand:
            return False
        return True


class Remodel(Card):
    types = [CardTypes.Action]
    card_cost = 4
    adhocturn_action_title = 'Trash a card? - Gain a card costing up to 2 more'
    adhocturn_form = RemodelForm

    def perform_specific_action(self, deck, turn):
        return QueuedTurn.objects.create(
            turn=turn,
            player=turn.player,
            game=turn.game,
            card=self,
        )

    def should_create_adhoc_turn(self, queued_turn):
        deck = queued_turn.game.decks.get(player=queued_turn.player)
        hand = deck.hand
        if not hand:
            return False
        return True


class Smithy(Card):
    types = [CardTypes.Action]
    card_cost = 4
    extra_cards = 3


class Spy(Card):
    types = [CardTypes.Action, CardTypes.Attack]
    card_cost = 4
    extra_actions = 1
    extra_cards = 1
    adhocturn_action_title = 'Discard?'
    adhocturn_form = SpyForm

    def perform_specific_action(self, deck, turn):
        queued_turns = []
        for player in deck.game.players.all():
            queued_turns.append(
                QueuedTurn.objects.create(
                    turn=turn,
                    player=turn.player,
                    game=turn.game,
                    card=self,
                    target_player=player,
                ),
            )
        queued_turns.append(
            QueuedTurn.objects.create(
                turn=turn,
                player=turn.player,
                game=turn.game,
                card=self,
                perform_simple_actions=True,
            ),
        )
        return queued_turns

    def should_create_adhoc_turn(self, queued_turn):
        player_deck = queued_turn.target_player.decks.get(game=queued_turn.game)
        if len(player_deck.draw_pile) < 1:
            player_deck.full_shuffle()
            player_deck.save()
            if len(player_deck.draw_pile) < 1:
                return False
        return True


# class Thief(Card):
#     pass


class ThroneRoom(Card):
    types = [CardTypes.Action]
    card_cost = 4
    adhocturn_action_title = 'Pick an action to play twice'
    adhocturn_form = ThroneRoomForm

    def perform_specific_action(self, deck, turn):
        return QueuedTurn.objects.create(
            turn=turn,
            player=turn.player,
            game=turn.game,
            card=self,
        )

    def should_create_adhoc_turn(self, queued_turn):
        player_deck = queued_turn.player.decks.get(game=queued_turn.game)
        if player_deck.no_actions:
            return False
        return True


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


class Workshop(Card):
    types = [CardTypes.Action]
    card_cost = 3
    adhocturn_action_title = 'Gain a card costing up to 4'
    adhocturn_form = WorkshopForm

    def perform_specific_action(self, deck, turn):
        return QueuedTurn.objects.create(
            turn=turn,
            player=turn.player,
            game=turn.game,
            card=self,
        )

    def should_create_adhoc_turn(self, queued_turn):
        return True
