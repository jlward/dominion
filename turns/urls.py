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

import turns.views
from turns.models import AdHocTurn, ReactionTurn

urlpatterns = [
    path(
        '<int:turn_id>',
        turns.views.end_phase,
        name='turns_end_phase',
    ),
    path(
        '<int:turn_id>/adhoc/perform_action',
        turns.views.perform_action,
        name='turns_adhocturn_adhoc_perform_action',
        kwargs=dict(Model=AdHocTurn),
    ),
    path(
        '<int:turn_id>/reaction/perform_action',
        turns.views.perform_action,
        name='turns_adhocturn_reaction_perform_action',
        kwargs=dict(Model=ReactionTurn),
    ),
]
