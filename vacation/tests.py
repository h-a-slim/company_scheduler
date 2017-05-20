from datetime import date

from django.test import TestCase

# Create your tests here.
from vacation.dates import generate_dates, exc_weekends


class VacationDurationTestCase(TestCase):
    def setUp(self):
        self.date_from = date(2017, 5, 20)
        self.date_to = date(2017, 5, 25)

    def test_duration_accept_all(self):
        dates = [x for x in generate_dates(date_from=self.date_from, date_to=self.date_to)]
        print(dates)
        self.assertEqual(len(dates), 5, "5 days must be generated")

    def test_duration_exclude_weekends(self):
        dates = [x for x in generate_dates(date_from=self.date_from, date_to=self.date_to, accept=exc_weekends)]
        print(dates)
        self.assertEqual(len(dates), 3, "3 days must be generated")
