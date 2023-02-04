from django import forms

from .base import BaseCardForm


class ChapelForm(BaseCardForm):
    source_object = 'deck'
    source_pile = 'real_hand'
    action = 'trash'
    min_cards = 0
    max_cards = 4
