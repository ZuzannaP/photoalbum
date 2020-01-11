from .models import Photo
from django import forms

class AddPhotoForm(forms.Form):
    path = forms.ImageField()


class LoginForm(forms.Form):
    username = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput, max_length=255)