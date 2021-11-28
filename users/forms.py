from django import forms
from .models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        help_text='<ul><li>allow emails from NTU, NUS and SMU</li></ul>'
    )
    #is_authority = forms.BooleanField()

    class Meta:
        model = User
        fields = ['username', 'is_authority', 'email', 'password1', 'password2']