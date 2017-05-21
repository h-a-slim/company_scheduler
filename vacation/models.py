"""
Vacation application, models.
"""

from django.contrib.auth.models import User
from django.db import models
from django.db.models import QuerySet
from math import ceil


class JsonSupportModel:
    """
    Abstract class to add support for json serialization
    """
    def to_dict(self):
        """
        Must be overridden to return a dictionary
        :return: dictionary representation of the object
        """
        raise NotImplementedError


class VacationModel(models.Model, JsonSupportModel):
    """
    Vacation Model with support for json serialization
    """
    date_from = models.DateField()
    date_to = models.DateField()
    description = models.CharField(max_length=100)
    duration = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def to_dict(self):
        return {
            'id': self.id,
            'date_from': self.date_from.strftime('%d-%m-%Y'),
            'date_to': self.date_to.strftime('%d-%m-%Y'),
            'description': self.description,
            'duration': self.duration
        }


class JqGridViewModel:
    """
    JqGridViewModel to be used with JqGrid, created in a generic way
    to support all JsonSupportModel objects
    """

    def __init__(self, query_set: QuerySet, page=1, rows_per_page=5):
        """
        Constructor
        :param query_set: the query set to use for the grid data
        :param page: the current page number to display
        :param rows_per_page: the number of rows per page
        """
        self._query_set = query_set
        self._records_count = self._query_set.count()
        self._rows_per_page = rows_per_page
        self._page = page

    def total_pages(self):
        return ceil(self._records_count / self._rows_per_page)

    def page(self):
        return self._page

    def records_count(self):
        return self._records_count

    def rows_array(self):
        begin = (self._page - 1) * self._rows_per_page
        end = begin + self._rows_per_page
        return [x.to_dict() for x in self._query_set[begin:end]]
