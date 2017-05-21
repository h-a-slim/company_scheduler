"""
Dates module to include useful utility methods while manipulating dates.
"""
from datetime import timedelta, date

'''
Filter weekdays using a lambda
'''
not_weekend = lambda d: d.weekday() < 5


def generate_dates(date_from=date, date_to=date, increment=timedelta(days=1)):
    """
    Generates a date on each call between @date_from and @date_to
    :param date_from: start generating from this date
    :param date_to: this date is excluded
    :param increment: timedelta increment default (1 day)
    :return: returns on each call a date object
    """
    iter_date = date_from
    while iter_date < date_to:
        yield iter_date
        iter_date += increment
