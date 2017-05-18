from django.shortcuts import render

from vacation.forms import LoginForm, RegisterForm


def index(request):
    login_form = LoginForm()
    register_form = RegisterForm()

    return render(request, 'auth/login.html', {
        'login_form': login_form,
        'register_form': register_form
    })



