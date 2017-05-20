from datetime import timedelta, date

exc_weekends = lambda d: d.weekday() < 5


def generate_dates(date_from=date, date_to=date, increment=timedelta(days=1), accept=lambda d: True):
    iter_date = date_from
    while iter_date < date_to:
        if accept(iter_date):
            yield iter_date
        iter_date += increment




