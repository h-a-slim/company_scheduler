from django.http import HttpResponseBadRequest
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse, HttpResponse, HttpResponseServerError
from django.shortcuts import render

from vacation.forms import LoginForm


def api_response(http_status_code=200, api_status='ok', api_response_body={}):
    return JsonResponse(status=http_status_code, data={'status': api_status, 'response': api_response_body})


def ok(body):
    return api_response(api_response_body=body)


def error(http_status_code, api_status='error', body='error occurred'):
    return api_response(http_status_code, api_status, {'error': body})


def login(request):
    if not request.method == 'POST':
        return error(HttpResponseBadRequest.status_code, body='request method not supported')

    login_form = LoginForm(request.POST)

    if login_form.is_valid():
        return ok('success')
    else:
        return error(HttpResponseBadRequest.status_code, body=login_form.errors)

    return error(HttpResponseServerError.status_code, body='request cannot be fulfilled at this time')


def register(request):
    if not request.method == 'POST':
        return error(HttpResponseBadRequest.status_code, body='request method not supported')

    register_form = LoginForm(request.POST)

    if register_form.is_valid():
        return ok('success')
    else:
        return error(HttpResponseBadRequest.status_code, body=register_form.errors)

    return error(HttpResponseServerError.status_code, body='request cannot be fulfilled at this time')

