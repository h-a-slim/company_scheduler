
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.http.response import JsonResponse, HttpResponseServerError

from vacation.dates import generate_dates, not_weekend
from vacation.forms import LoginForm, RegisterForm, VacationDuration, ApplyToVacationForm
from vacation.models import VacationModel


def api_response(http_status_code=200, api_status='ok', api_response_body={}):
    return JsonResponse(status=http_status_code, data={'status': api_status, 'response': api_response_body})


def ok(body):
    return api_response(api_response_body=body)


def error(http_status_code, api_status='error', body='error occurred'):
    return api_response(http_status_code, api_status, {'error': body})


def only_post(api_operation):
    def call_if_post(request):
        if not request.method == 'POST':
            return error(HttpResponseBadRequest.status_code, body='request method not supported')
        return api_operation(request)

    return call_if_post


def only_authenticated(api_operation):
    def call_if_authenticated(request):
        if not request.user.is_authenticated:
            return error(HttpResponseBadRequest.status_code, body='sign in please')
        return api_operation(request)

    return call_if_authenticated


@only_post
def signin(request):
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


@only_post
def register(request):
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


@only_post
@only_authenticated
def duration(request):
    vacation_form = VacationDuration(request.POST)
    if vacation_form.is_valid():
        vacation_form.clean()
        date_from = vacation_form.cleaned_data['date_from']
        date_to = vacation_form.cleaned_data['date_to']

        if date_from > date_to:
            return error(HttpResponseBadRequest.status_code, body='date from cannot be greater than date till')

        nb_days = sum(map(not_weekend, generate_dates(date_from=date_from, date_to=date_to)))

        if nb_days <= 0:
            return error(HttpResponseBadRequest.status_code, body='please check your dates')

        return ok({'duration': nb_days})
    else:
        return error(HttpResponseBadRequest.status_code, body=vacation_form.errors)

    return error(HttpResponseServerError.status_code, body='request cannot be fulfilled at this time')


@only_post
@only_authenticated
def apply(request):
    apply_form = ApplyToVacationForm(request.POST)

    if apply_form.is_valid():
        apply_form.clean()

        date_from = apply_form.cleaned_data['date_from']
        date_to = apply_form.cleaned_data['date_to']
        description = apply_form.cleaned_data['description']

        if date_from > date_to:
            return error(HttpResponseBadRequest.status_code, body='date from cannot be greater than date till')

        nb_days = sum(map(not_weekend, generate_dates(date_from=date_from, date_to=date_to)))
        if nb_days <= 0:
            return error(HttpResponseBadRequest.status_code, body='please check your dates')

        vacation = VacationModel(date_from=date_from, date_to=date_to, description=description, user=request.user)
        vacation.save()

        return ok(body='success')
    else:
        return error(HttpResponseBadRequest.status_code, body=apply_form.errors)

    return error(HttpResponseServerError.status_code, body='request cannot be fulfilled at this time')

