from django.urls import path

import accounts.views

urlpatterns = [
    path('login', accounts.views.login, name='accounts_login'),
]
