"""
Vacation application, views
"""

from django.http.response import HttpResponseRedirect
from django.shortcuts import render

from vacation.forms import LoginForm, RegisterForm, ApplyToVacationForm


def index(request):
    login_form = LoginForm()
    register_form = RegisterForm()

    return render(request, 'vacation/login.html', {
        'login_form': login_form,
        'register_form': register_form
    })


def schedule(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/vacation')

    form = ApplyToVacationForm()
    return render(request, 'vacation/schedule.html', {'form': form})
