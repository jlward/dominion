from django.contrib import admin
from django.urls import include, path

import accounts.views

urlpatterns = [
    path('login', accounts.views.login, name='accounts_login'),
]
