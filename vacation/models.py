"""
Vacation application, models.
"""

from django.contrib.auth.models import User
from django.db import models


class VacationModel(models.Model):
    date_from = models.DateField()
    date_to = models.DateField()
    description = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
