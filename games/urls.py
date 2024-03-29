"""dominion URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

import games.views

urlpatterns = [
    path('', games.views.game_list, name='game_list'),
    path('create', games.views.game_create, name='game_create'),
    path(
        '<int:game_id>',
        games.views.play_game_as_player,
        name='games_play',
    ),
    path(
        '<int:game_id>/game_hash',
        games.views.game_hash,
        name='game_hash',
    ),
    path(
        '<int:game_id>/play_action',
        games.views.play_action,
        name='games_play_action',
    ),
    path(
        '<int:game_id>/play_treasure',
        games.views.play_treasure,
        name='games_play_treasure',
    ),
    path(
        '<int:game_id>/play_all_treasures',
        games.views.play_all_treasures,
        name='games_play_all_treasures',
    ),
    path(
        '<int:game_id>/buy_kingdom_card',
        games.views.buy_kingdom_card,
        name='games_buy_kingdom_card',
    ),
]
