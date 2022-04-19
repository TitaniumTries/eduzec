from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, UserChangeForm
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", 'email',)


class CustomUserChangeForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "first_name", "last_name", "hide_email",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].help_text += " If you change your email, you have to verify it again and you will be logged out!"


class CustomUserAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='Username or Email',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    error_messages = {
        **AuthenticationForm.error_messages,
        'invalid_login': _(
            "Please enter a correct username or email, and password. Note that both fields may be case-sensitive."
        ),
    }

class ResendEmailVerificationForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ("email",)