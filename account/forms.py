from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms

from .models import OneTimeCode
class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")

    class Meta:
        model = User
        fields = ("username",
                  "email",
                  "password1",
                  "password2", )

class ConfirmPassword(forms.ModelForm):

    class Meta:
        model = OneTimeCode
        fields = ('code',)