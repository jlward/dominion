from django.templatetags.static import static

from cards.constants import CardTypes
from turns.models import StackedTurn, Turn


class Card:
    extra_buys = 0
    extra_actions = 0
    extra_cards = 0
    extra_treasure = 0
    extra_victory_points = 0
    cards_in_pile = 10
    unlimited = False
    adhocturn_action_title = ''
    adhocturn_form = None

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def plus_buys(self, *args, **kwargs):
        return self.extra_buys

    @property
    def plus_actions(self, *args, **kwargs):
        return self.extra_actions

    @property
    def plus_cards(self, *args, **kwargs):
        return self.extra_cards

    @property
    def plus_treasures(self, *args, **kwargs):
        return self.extra_treasure

    def get_victory_points(self, deck, *args, **kwargs):
        return self.extra_victory_points

    @property
    def cost(self):
        # `card_cost` is not set on purpose. We want this to always be explicitly set.
        return self.card_cost

    @property
    def types(self):
        raise NotImplementedError()

    @property
    def is_action(self):
        return CardTypes.Action in self.types

    @property
    def is_treasure(self):
        return CardTypes.Treasure in self.types

    @property
    def is_victory(self):
        return CardTypes.Victory in self.types

    @property
    def is_base_card(self):
        base_cards = [
            'Copper',
            'Silver',
            'Gold',
            'Platinum',
            'Estate',
            'Duchy',
            'Province',
            'Colony',
            'Curse',
        ]
        if self.name in base_cards:
            return True
        return False

    @property
    def path(self):
        return f'images/{self.name}.jpg'

    @property
    def url(self):
        return static(self.path)

    def _perform_simple_actions(self, deck, turn):
        deck.draw_cards(self.plus_cards)
        turn.available_actions += self.plus_actions
        turn.available_buys += self.plus_buys
        turn.available_money += self.plus_treasures
        deck.save()
        turn.save()

    def perform_specific_actions(self, deck, turn):
        pass

    def execute_card(self, deck, turn):
        self._perform_simple_actions(deck, turn)
        self.perform_specific_actions(deck, turn)

    def create_stacked_turns(self, deck, turn):
        return StackedTurn.objects.create(
            turn=turn,
            player=turn.player,
            game=turn.game,
            card=self,
            perform_simple_actions=True,
        )

    def play_action(self, deck, turn: Turn):
        self.create_stacked_turns(deck, turn)

    def should_create_adhoc_turn(self, stacked_turn):
        raise NotImplementedError()  # pragma: no cover

    def __str__(self):
        return self.name
