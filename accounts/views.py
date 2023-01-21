from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.shortcuts import redirect, render

from .forms import LoginForm


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            if user is not None:
                django_login(request, user)
                return redirect('game_list')

    context = dict(
        form=form,
    )
    return render(request, 'login.html', context)
