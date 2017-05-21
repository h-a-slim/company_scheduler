"""
Vacation application, Forms.
These forms are used in views as well as apis.
"""

from django import forms

from company_site import settings


class LoginForm(forms.Form):
    """
    Login form used in @vacation.views and @vacation.api.signin
    """
    user_name = forms.EmailField(max_length=30, widget=forms.EmailInput(
        attrs={'class': 'form-control',
               'data-validation': 'email required'
               }
    ))

    user_password = forms.CharField(max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'data-validation': 'length alphanumeric required',
               'data-validation-length': 'min8'
               }
    ))


class RegisterForm(forms.Form):
    """
    Registration form used in @vacation.views and @vacation.api.register
    """
    user_name = forms.EmailField(min_length=5, max_length=30, widget=forms.EmailInput(
        attrs={'class': 'form-control',
               'data-validation': 'email length required',
               'data-validation-length': '5-30'
               }
    ))

    user_password = forms.CharField(min_length=8, max_length=20, widget=forms.PasswordInput(
        attrs={'class': 'form-control',
               'data-validation': 'length alphanumeric required',
               'data-validation-length': '8-20'
               }
    ))

    user_fname = forms.CharField(min_length=3, max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'data-validation': 'length alphanumeric required',
               'data-validation-length': '3-20'
               }
    ))

    user_lname = forms.CharField(min_length=3, max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'data-validation': 'length alphanumeric required',
               'data-validation-length': '3-20'
               }
    ))


class ApplyToVacationForm(forms.Form):
    """
    Apply to vacation form, used in @vacation.views and @vacation.api.apply
    """
    date_from = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=forms.DateInput(
        attrs={
            'class': 'form-control',
            'data-validation': 'date required',
            'data-validation-format': 'dd-mm-yyyy'
        }
    ))

    date_to = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS, widget=forms.DateInput(
        attrs={
            'class': 'form-control',
            'data-validation': 'date required',
            'data-validation-format': 'dd-mm-yyyy'
        }
    ))

    description = forms.CharField(max_length=100, min_length=10, widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'data-validation': 'length alphanumeric required',
            'data-validation-allowing': "-_.;",
            'data-validation-length': '10-100'
        }
    ))


class VacationDuration(forms.Form):
    """
    Calculate vacation duration form, used in @vacation.api.duration
    """
    date_from = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
    date_to = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)

