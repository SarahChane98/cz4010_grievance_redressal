from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    #is_authority = forms.BooleanField()

    class Meta:
        model = User
        fields = ['username', 'is_authority', 'email', 'password1', 'password2']