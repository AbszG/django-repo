from django import forms
from django.contrib.auth.forms import AuthenticationForm

class UserLoginForm(AuthenticationForm):
    #additional options at Django Docs
    username = forms.CharField(label="Username", max_length=30)
    password = forms.CharField(label="Password", max_length=30, widget=forms.PasswordInput)