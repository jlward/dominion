from django import template

register = template.Library()


@register.inclusion_tag('cards/card.html', takes_context=True)
def card_in_hand(context, card, *args, **kwargs):
    return dict(card=card, turn=context['turn'], game=context['game'], in_hand=True)


@register.inclusion_tag('cards/card.html', takes_context=True)
def card_in_play(context, card, *args, **kwargs):
    return dict(card=card, turn=context['turn'], game=context['game'], in_hand=False)


@register.inclusion_tag('cards/card.html', takes_context=True)
def card_in_kingdom(context, card, *args, **kwargs):
    return dict(
        card=card['card'],
        turn=context['turn'],
        game=context['game'],
        in_kingdom=True,
        count=card['count'],
    )
