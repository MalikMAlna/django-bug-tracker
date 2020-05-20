from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Account

# Code Citation: https://www.youtube.com/
# watch?v=oZUb372g6Do&list=PLgCYzUzKIBE_dil025VAJnDjNZHHHR9mW&index=14S


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        max_length=60, help_text="Required: Please add a valid email address.")

    class Meta:
        model = Account
        fields = ('email', 'username', 'display_name',
                  'age', 'password1', 'password2')


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=25, help_text='*Required')
    password = forms.CharField(
        widget=forms.PasswordInput,
        help_text='*Required'
    )
