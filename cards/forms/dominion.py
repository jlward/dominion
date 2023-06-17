from django import forms

from cards import get_card_from_name, get_cards_from_names
from cards.forms.base.simple import SimpleForm
from cards.kingdom_cards.base_cards import Copper
from turns.models import StackedTurn

from .base.choose_cards import ChooseCardsForm


class BureaucratForm(ChooseCardsForm):
    source_object = 'deck'
    source_pile = 'hand'
    min_cards = 1
    max_cards = 1
    card_filter = 'is_victory'

    def save(self):
        cards = self.cleaned_data['cards']

        deck = self.adhoc_turn.player.decks.get(game=self.game)
        deck.move_to_top_deck(cards[0])
        deck.save()


class ChapelForm(ChooseCardsForm):
    source_object = 'deck'
    source_pile = 'hand'
    actions = ['trash']
    min_cards = 0
    max_cards = 4


class CellarForm(ChooseCardsForm):
    source_object = 'deck'
    source_pile = 'hand'
    min_cards = 0
    max_cards = 1000

    def save(self):
        self.deck.discard_cards(self.cleaned_data['cards'])
        self.deck.draw_cards(len(self.cleaned_data['cards']))
        self.deck.save()


class ChancellorForm(SimpleForm):
    def save(self):
        if self.cleaned_data['selection'] != self.selection_yes:
            return
        self.deck.discard_pile.extend(self.deck.draw_pile)
        self.deck.draw_pile = []
        self.deck.save()


class FeastForm(ChooseCardsForm):
    source_object = 'game'
    source_pile = 'kingdom_options'
    min_cards = 1
    max_cards = 1

    def get_source_pile(self):
        source_pile = super().get_source_pile()
        return [card for card in source_pile if card.cost <= 5]

    def save(self):
        self.game.gain_card(self.deck, self.cleaned_data['cards'][0])
        self.deck.save()
        self.game.save()


class LibraryForm(SimpleForm):
    def cards_to_display(self):
        deck = self.game.decks.get(
            player=self.adhoc_turn.player,
        )
        card_name = deck.draw_pile.pop(0)
        return get_cards_from_names([card_name])

    def save(self):
        deck = self.game.decks.get(
            player=self.adhoc_turn.player,
        )
        if self.cleaned_data['selection'] == self.selection_yes:
            deck.draw_cards(1)
        else:
            deck.draw_cards(1, destination='narnia_pile')
        if len(deck.hand) < 7:
            StackedTurn.objects.create(
                turn=self.turn,
                player=self.player,
                game=self.game,
                card=self.adhoc_turn.card,
            )
        else:
            deck.discard_pile.extend(deck.narnia_pile)
            deck.narnia_pile = []
        deck.save()


class MilitiaForm(ChooseCardsForm):
    source_object = 'deck'
    source_pile = 'hand'
    max_cards = 3

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.min_cards = min([3, len(self.deck.hand)])

    def save(self):
        hand_copy = self.deck.hand[:]
        for card in self.cleaned_data['cards']:
            hand_copy.remove(card.name)

        self.deck.discard_cards(get_cards_from_names(hand_copy))
        self.deck.save()


class MineForm(ChooseCardsForm):
    source_object = 'deck'
    source_pile = 'hand'
    min_cards = 0
    max_cards = 1
    actions = ['trash']
    kingdom_card = forms.ChoiceField(
        choices=[],
        widget=forms.RadioSelect(
            attrs={
                'class': 'kingdom-selector',
            },
        ),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        kingdom_cards = [card for card in self.game.kingdom_options if card.is_treasure]
        self.fields['kingdom_card'].choices = self.format_cards(kingdom_cards)
        self.fields['cards'].label = 'Hand'

    def get_source_pile(self):
        hand = super().get_source_pile()
        return [card for card in hand if card.is_treasure]

    def clean_kingdom_card(self):
        kingdom_card = self.cleaned_data['kingdom_card']
        hand_cards = self.cleaned_data.get('cards')
        if not hand_cards:
            if kingdom_card:
                raise forms.ValidationError('No trash card selected')
            return self.cleaned_data['kingdom_card']
        if not kingdom_card:
            raise forms.ValidationError('No gain card selected')
        self.cleaned_data['kingdom_card'] = get_cards_from_names([kingdom_card])[0]
        hand_card = hand_cards[0]
        if hand_card.cost + 3 < self.cleaned_data['kingdom_card'].cost:
            raise forms.ValidationError('kingdom card seleceted is too expensive')
        return self.cleaned_data['kingdom_card']

    def save(self):
        super().save()
        if not self.cleaned_data['cards']:
            return
        kingdom_card = self.cleaned_data['kingdom_card']
        self.game.gain_card(self.deck, kingdom_card)
        self.deck.save()


class MoneylenderForm(SimpleForm):
    def save(self):
        if self.cleaned_data['selection'] != self.selection_yes:
            return
        self.deck.trash_cards([Copper()])
        self.turn.available_money += 3
        self.deck.save()
        self.turn.save()


class RemodelForm(ChooseCardsForm):
    source_object = 'deck'
    source_pile = 'hand'
    min_cards = 1
    max_cards = 1
    actions = ['trash']
    kingdom_card = forms.ChoiceField(
        choices=[],
        widget=forms.RadioSelect(
            attrs={
                'class': 'kingdom-selector',
            },
        ),
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        kingdom_cards = [card for card in self.game.kingdom_options]
        self.fields['kingdom_card'].choices = self.format_cards(kingdom_cards)
        self.fields['cards'].label = 'Hand'

    def get_source_pile(self):
        hand = super().get_source_pile()
        return [card for card in hand]

    def clean_kingdom_card(self):
        kingdom_card = self.cleaned_data['kingdom_card']
        hand_cards = self.cleaned_data.get('cards')
        if not hand_cards:
            return self.cleaned_data['kingdom_card']
        self.cleaned_data['kingdom_card'] = get_cards_from_names([kingdom_card])[0]
        hand_card = hand_cards[0]
        if hand_card.cost + 2 < self.cleaned_data['kingdom_card'].cost:
            raise forms.ValidationError('kingdom card seleceted is too expensive')
        return self.cleaned_data['kingdom_card']

    def save(self):
        super().save()
        kingdom_card = self.cleaned_data['kingdom_card']
        self.game.gain_card(self.deck, kingdom_card)
        self.deck.save()


class SpyForm(SimpleForm):
    def extra_info(self):
        target_player = self.adhoc_turn.target_player
        return f"This is {target_player}'s deck"

    def cards_to_display(self):
        deck = self.game.decks.get(
            player=self.adhoc_turn.target_player,
        )
        card_name = deck.draw_pile.pop(0)
        return get_cards_from_names([card_name])

    def save(self):
        if self.cleaned_data['selection'] != self.selection_yes:
            return
        target_deck = self.game.decks.get(player=self.adhoc_turn.target_player)
        target_deck.draw_cards(1, destination='discard_pile')
        target_deck.save()


class ThiefForm(ChooseCardsForm):
    source_object = 'target_player_deck'
    source_pile = 'narnia_pile'
    min_cards = 1
    max_cards = 1

    def save(self):
        for card in self.cleaned_data['cards']:
            self.target_player_deck.move_to_discard(card, source='narnia_pile')
        self.target_player_deck.save()

    def clean_cards(self):
        # form returns selected card. need to get unselected card to discard
        card = super().clean_cards()[0]
        narnia_cards = [item.name for item in self.get_source_pile()]
        narnia_cards.pop(narnia_cards.index(card.name))
        self.cleaned_data['cards'] = [get_card_from_name(narnia_cards[0])]
        return self.cleaned_data['cards']


class ThiefCleanupForm(ChooseCardsForm):
    source_object = 'game'
    source_pile = 'narnias'
    min_cards = 0

    @property
    def max_cards(self):
        return len(self.get_source_pile())

    def save(self):
        self.game.move_cards_from_narnias_to_player(
            cards=self.cleaned_data['cards'],
            player=self.player,
            destination='discard_pile',
        )
        self.game.trash_narnias()


class ThroneRoomForm(ChooseCardsForm):
    source_object = 'deck'
    source_pile = 'hand'
    min_cards = 0
    max_cards = 1

    def get_source_pile(self):
        hand = super().get_source_pile()
        return [card for card in hand if card.is_action]

    def save(self):
        for card in self.cleaned_data['cards']:
            self.turn.play_action(card, consume=False)
            self.turn.play_action(card, consume=False, ghost_action=True)


class WorkshopForm(ChooseCardsForm):
    source_object = 'game'
    source_pile = 'kingdom_options'
    min_cards = 1
    max_cards = 1

    def get_source_pile(self):
        source_pile = super().get_source_pile()
        return [card for card in source_pile if card.cost <= 4]

    def save(self):
        self.game.gain_card(self.deck, self.cleaned_data['cards'][0])
        self.deck.save()
        self.game.save()
