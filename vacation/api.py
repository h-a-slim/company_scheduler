from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.http.response import JsonResponse, HttpResponseServerError

from vacation.dates import generate_dates, exc_weekends
from vacation.forms import LoginForm, RegisterForm, VacationDuration, ApplyToVacationForm


def api_response(http_status_code=200, api_status='ok', api_response_body={}):
    return JsonResponse(status=http_status_code, data={'status': api_status, 'response': api_response_body})


def ok(body):
    return api_response(api_response_body=body)


def error(http_status_code, api_status='error', body='error occurred'):
    return api_response(http_status_code, api_status, {'error': body})


def signin(request):
    if not request.method == 'POST':
        return error(HttpResponseBadRequest.status_code, body='request method not supported')

    login_form = LoginForm(request.POST)

    if login_form.is_valid():
        login_form.clean()
        user = authenticate(request, username=login_form.cleaned_data['user_name'], password=login_form.cleaned_data['user_password'])
        if user is not None:
            login(request, user)
            return ok('success')
        else:
            return error(HttpResponseBadRequest.status_code, body='invalid username/password')
    else:
        return error(HttpResponseBadRequest.status_code, body=login_form.errors)

    return error(HttpResponseServerError.status_code, body='request cannot be fulfilled at this time')


def register(request):
    if not request.method == 'POST':
        return error(HttpResponseBadRequest.status_code, body='request method not supported')

    register_form = RegisterForm(request.POST)

    if register_form.is_valid():
        register_form.clean()

        user = User.objects.create_user(
            register_form.cleaned_data['user_name'],
            register_form.cleaned_data['user_name'],
            register_form.cleaned_data['user_password'])

        user.first_name = register_form.cleaned_data['user_fname']
        user.last_name = register_form.cleaned_data['user_fname']
        user.save()
        return ok('success')
    else:
        return error(HttpResponseBadRequest.status_code, body=register_form.errors)

    return error(HttpResponseServerError.status_code, body='request cannot be fulfilled at this time')


def duration(request):
    if not request.method == 'POST':
        return error(HttpResponseBadRequest.status_code, body='request method not supported')

    vacation_form = VacationDuration(request.POST)
    if vacation_form.is_valid():
        vacation_form.clean()
        date_from = vacation_form.cleaned_data['date_from']
        date_to = vacation_form.cleaned_data['date_to']

        if date_from > date_to:
            return error(HttpResponseBadRequest.status_code, body='date from cannot be greater than date till')

        dates = [x for x in generate_dates(date_from=date_from, date_to=date_to, accept=exc_weekends)]
        return ok({'duration': len(dates)})
    else:
        return error(HttpResponseBadRequest.status_code, body=vacation_form.errors)

    return error(HttpResponseServerError.status_code, body='request cannot be fulfilled at this time')


def apply(request):
    if not request.method == 'POST':
        return error(HttpResponseBadRequest.status_code, body='request method not supported')

    apply_form = ApplyToVacationForm(request.POST)
    if apply_form.is_valid():
        apply_form.clean()

        date_from = apply_form.cleaned_data['date_from']
        date_to = apply_form.cleaned_data['date_to']

        if date_from > date_to:
            return error(HttpResponseBadRequest.status_code, body='date from cannot be greater than date till')

        dates = [x for x in generate_dates(date_from=date_from, date_to=date_to, accept=exc_weekends)]
        return ok({'duration': len(dates)})
    else:
        return error(HttpResponseBadRequest.status_code, body=apply_form.errors)

    return error(HttpResponseServerError.status_code, body='request cannot be fulfilled at this time')

