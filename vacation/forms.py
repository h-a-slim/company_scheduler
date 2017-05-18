from django import forms


class LoginForm(forms.Form):
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

    user_fname = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'data-validation': 'length alphanumeric required',
               'data-validation-length': 'min3'
               }
    ))

    user_lname = forms.CharField(max_length=20, widget=forms.TextInput(
        attrs={'class': 'form-control',
               'data-validation': 'length alphanumeric required',
               'data-validation-length': 'min3'
               }
    ))
