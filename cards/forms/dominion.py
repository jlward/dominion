from django import forms

from cards import get_cards_from_names
from cards.forms.base.simple import SimpleForm
from cards.kingdom_cards.base_cards import Copper

from .base.choose_cards import ChooseCardsForm


class ChapelForm(ChooseCardsForm):
    source_object = 'deck'
    source_pile = 'real_hand'
    actions = ['trash']
    min_cards = 0
    max_cards = 4


class CellarForm(ChooseCardsForm):
    source_object = 'deck'
    source_pile = 'real_hand'
    min_cards = 0
    max_cards = 1000

    def save(self):
        self.deck.discard_cards(self.cleaned_data['cards'])
        self.deck.draw_cards(len(self.cleaned_data['cards']))
        self.deck.save()


class MoneylenderForm(SimpleForm):
    def save(self):
        if self.cleaned_data['selection'] != '0':
            return
        self.deck.trash_cards([Copper()])
        self.turn.available_money += 3
        self.deck.save()
        self.turn.save()


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


class SpyForm(SimpleForm):
    def extra_info(self):
        target_player = self.adhoc_turn.target_player
        return f"This is {target_player}'s deck"

    def cards_to_display(self):
        deck = self.game.decks.get(
            player=self.adhoc_turn.target_player,
        )
        if len(deck.draw_pile) < 1:
            deck.full_shuffle()
            deck.save()
            if len(deck.draw_pile) < 1:
                return
        card_name = deck.draw_pile.pop(0)
        return get_cards_from_names([card_name])

    def save(self):
        if self.cleaned_data['selection'] != '0':
            return
        target_deck = self.game.decks.get(player=self.adhoc_turn.target_player)
        target_deck.draw_cards(1, destination='discard_pile')
        target_deck.save()


class MineForm(ChooseCardsForm):
    source_object = 'deck'
    source_pile = 'real_hand'
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


class ThroneRoomForm(ChooseCardsForm):
    source_object = 'deck'
    source_pile = 'real_hand'
    min_cards = 0
    max_cards = 1

    def get_source_pile(self):
        hand = super().get_source_pile()
        return [card for card in hand if card.is_action]

    def save(self):
        for card in self.cleaned_data['cards']:
            self.turn.play_action(card, consume=False)
            self.turn.play_action(card, consume=False, ghost_action=True)


class RemodelForm(ChooseCardsForm):
    source_object = 'deck'
    source_pile = 'real_hand'
    # TODO empty hand check
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
        required=False,
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
            if kingdom_card:
                raise forms.ValidationError('No trash card selected')
            return self.cleaned_data['kingdom_card']
        if not kingdom_card:
            raise forms.ValidationError('No gain card selected')
        self.cleaned_data['kingdom_card'] = get_cards_from_names([kingdom_card])[0]
        hand_card = hand_cards[0]
        if hand_card.cost + 2 < self.cleaned_data['kingdom_card'].cost:
            raise forms.ValidationError('kingdom card seleceted is too expensive')
        return self.cleaned_data['kingdom_card']

    def save(self):
        super().save()
        if not self.cleaned_data['cards']:
            return
        kingdom_card = self.cleaned_data['kingdom_card']
        self.game.gain_card(self.deck, kingdom_card)
        self.deck.save()


class ChancellorForm(SimpleForm):
    def save(self):
        if self.cleaned_data['selection'] != '0':
            return
        self.deck.discard_pile.extend(self.deck.draw_pile)
        self.deck.draw_pile = []
        self.deck.save()
