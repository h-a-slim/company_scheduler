from datetime import timedelta, date

not_weekend = lambda d: d.weekday() < 5


def generate_dates(date_from=date, date_to=date, increment=timedelta(days=1)):
    iter_date = date_from
    while iter_date < date_to:
        yield iter_date
        iter_date += increment
