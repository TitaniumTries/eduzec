from urllib import request
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordResetForm
from django.forms import ModelForm
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe

from .models import CustomUser

from django.core.exceptions import ValidationError
from .utilities import send_verification_email
from django.contrib.auth import authenticate


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("username", 'email',)


class CustomUserChangeForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email", "avatar", "first_name", "last_name", "hide_email",)

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
            mark_safe("Please enter a correct username or email, and password.<br/>Note that both fields may be case-sensitive.")
        ),
    }

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username is not None and password:
            self.user_cache = authenticate(
                self.request, username=username, password=password
            )
            if self.user_cache is None:
                self.add_error('username', ValidationError(
                    self.error_messages["invalid_login"],
                    code="invalid_login",
                    params={"username": self.username_field.verbose_name},
                ))
                self.add_error('password', '')
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data


class ResendEmailVerificationForm(forms.Form):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email"}),
    )

    error_messages = {
        "user_not_found": _("User with this email not found!"),
        "email_already_verified": _("User\'s email already verified!"),
    }

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            self.user = CustomUser.objects.get(email__iexact=email)
        except Exception as e:
            self.user = None

        if self.user:
            if self.user.email_verified == True:
                raise ValidationError(
                    self.error_messages["email_already_verified"],
                    code="email_already_verified",
                )
        else:
            raise ValidationError(
                self.error_messages["user_not_found"],
                code="user_not_found",
            )

        return email
    
    def save(self, request):        
        send_verification_email(request, self.user)


class CustomPasswordResetForm(PasswordResetForm):
    error_messages = {
        "user_not_found": _("User with this email not found!"),
        "email_not_verified": _("User's email is not verified!"),
    }

    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            self.user = CustomUser.objects.get(email__iexact=email)
        except Exception as e:
            self.user = None

        if self.user:
            if self.user.email_verified == False:
                raise ValidationError(
                    self.error_messages["email_not_verified"],
                    code="email_not_verified",
                )
        else:
            raise ValidationError(
                self.error_messages["user_not_found"],
                code="user_not_found",
            )

        return email