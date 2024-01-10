from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control p-2 mb-2',
                'placeholder': 'Username'
            }
        ),
    )
    password = forms.CharField(
        label='',
        max_length=100,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control p-2 mb-2',
                'placeholder': 'Password'
            }
        ),
    )


class SignupForm(UserCreationForm):
    username = forms.CharField(
        label='',
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control p-2 mb-2',
                'placeholder': 'Username'
            }
        )
    )

    password1 = forms.CharField(
        label='',
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control p-2 mb-2',
                'placeholder': 'Password'
            }
        ))

    password2 = forms.CharField(
        label='',
        max_length=100,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control p-2 mb-2',
                'placeholder': 'Confirm Password'
            }
        ))
