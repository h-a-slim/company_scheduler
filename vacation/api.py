"""
Vacation application, Api module.
Contains operations that returns json as response.
Current implementation uses Django forms for the request to simplify the validation.
"""

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest
from django.http.response import JsonResponse, HttpResponseServerError

from vacation.dates import generate_dates, not_weekend
from vacation.forms import LoginForm, RegisterForm, VacationDuration, ApplyToVacationForm
from vacation.models import VacationModel, JqGridViewModel


def api_response(http_status_code=200, api_status='ok', api_response_body={}):
    """
    The generic Api response function that can be customized for different responses.
    :param http_status_code: the http status to be returned example: 200
    :param api_status: the api status to be returned
    :param api_response_body: the actual api response maybe a string or a json object
    :return: returns the response as a json object
    """
    return JsonResponse(status=http_status_code, data={'status': api_status, 'response': api_response_body})


def ok(body):
    """
    Specific implementation for the @api_response function, mainly used to signify success.
    :param body: check @api_response
    :return: check @api_response
    """
    return api_response(api_response_body=body)


def error(http_status_code, api_status='error', body='error occurred'):
    """
    Specific implementation for the @api_response function, mainly used to signify an error.
    :param http_status_code: check @api_response
    :param api_status: check @api_response
    :param body: check @api_response
    :return: check @api_response
    """
    return api_response(http_status_code, api_status, {'error': body})


def only_post(api_operation):
    """
    Decorator for Api functions to restrict the http method to POST only.
    :param api_operation: the Api function to be decorated
    :return: an Api error or calls the Api function
    """

    def call_if_post(request):
        if not request.method == 'POST':
            return error(HttpResponseBadRequest.status_code, body='request method not supported')
        return api_operation(request)

    return call_if_post


def only_authenticated(api_operation):
    """
    Decorator for Api functions to restrict access to authenticated usres only
    :param api_operation: the Api function to be decorated
    :return: an Api error or calls the Api function
    """

    def call_if_authenticated(request):
        if not request.user.is_authenticated:
            return error(HttpResponseBadRequest.status_code, body='sign in please')
        return api_operation(request)

    return call_if_authenticated


@only_post
def signin(request):
    """
    Api method to signin the user, uses Django auth to handle authentication.
    :param request:
    :return: @api_response
    """
    login_form = LoginForm(request.POST)

    if login_form.is_valid():
        login_form.clean()
        user = authenticate(request, username=login_form.cleaned_data['user_name'],
                            password=login_form.cleaned_data['user_password'])
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
    """
    Api method to register the user.
    :param request:
    :return: @api_response
    """
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
    """
    Api method to calculate the vacation duration, uses the @vacation.generate_dates.
    :param request:
    :return: @api_response
    """
    vacation_form = VacationDuration(request.POST)
    if vacation_form.is_valid():
        vacation_form.clean()
        date_from = vacation_form.cleaned_data['date_from']
        date_to = vacation_form.cleaned_data['date_to']

        if date_from > date_to:
            return error(HttpResponseBadRequest.status_code, body='date from cannot be greater than date till')

        '''
        Using an iterable from the generation function, passed to a map function to filter
        non weekdays, and then the boolean result is summed with sum. At each iteration,
        a new element is generated passed to map then sum. Thus avoiding creating a list, then
        counting the elements. It should theoretically run in O(n) worst case when all dates are actually
        weekdays where n is number of days included between date_from and date_to.
        '''
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
    """
    Api method used to add a vacation record to the database after validation and checking the number of days
    is strictly greater than zero.
    :param request:
    :return: @api_response
    """
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

        vacation = VacationModel(
            date_from=date_from, date_to=date_to, description=description, user=request.user, duration=nb_days)
        vacation.save()

        return ok(body='success')
    else:
        return error(HttpResponseBadRequest.status_code, body=apply_form.errors)

    return error(HttpResponseServerError.status_code, body='request cannot be fulfilled at this time')


@only_authenticated
def employee_vacations(request):
    """
    Api method used to retrieve all vacations for the singed in user.
    It returns a JqGrid json object on success.
    reference: http://www.trirand.com/jqgridwiki/doku.php?id=wiki:retrieving_data
    :param request:
    :return: @api_response
    """
    current_page = int(request.GET['page'])
    rows_per_page = int(request.GET['rows'])

    if current_page <= 0 or rows_per_page <= 0:
        return error(HttpResponseBadRequest.status_code, body='bad request')

    jqgrid = JqGridViewModel(query_set=VacationModel.objects.filter(user=request.user), page=current_page, rows_per_page=rows_per_page)

    jqgrid_json = {
        "total": jqgrid.total_pages(),
        "page": jqgrid.page(),
        "records": jqgrid.records_count(),
        "rows": jqgrid.rows_array()
    }

    return ok(body=jqgrid_json)
