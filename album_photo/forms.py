from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User

from .models import Photo
from django import forms

class AddPhotoForm(forms.Form):
    path = forms.ImageField()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput, max_length=255)


class CustomUserChangeForm(UserChangeForm):
    # UserChangeForm wywołuje hasło, dlatego trzeba to nadpisać ustawiając "None"
    password = None

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
