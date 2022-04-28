import re
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import FormView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render

from users.forms import CustomUserCreationForm, CustomUserChangeForm, CustomUserAuthenticationForm, ResendEmailVerificationForm
from django.contrib.auth.views import LoginView
from users.models import CustomUser

from django.contrib.auth import login as auth_login
from django.contrib.auth.views import logout_then_login
from django.contrib.auth import logout as auth_logout
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .utilities import generate_token, send_verification_email

from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView

INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"
from django.core.exceptions import ImproperlyConfigured
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters

from django.utils.safestring import mark_safe
from django.contrib.auth import update_session_auth_hash

class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('users:login')
    form_class = CustomUserCreationForm

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        send_verification_email(self.request, self.object)

        messages.success(self.request, "%s, your profile was created successfully." % self.object.username)
        messages.info(self.request, 'Please verify your email to log in!')
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:dashboard')

        return super().dispatch(request, *args, **kwargs)

class EditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'users/edit_account.html'
    success_url = reverse_lazy('users:edit_account')
    form_class = CustomUserChangeForm
    success_message = "Successfully updated profile."

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        user = self.get_object() # this gets the user from the DB
        if (user.email != self.object.email): #self.object contains the user from the form
            self.object.email_verified = False
            send_verification_email(self.request, self.object)
            messages.info(self.request, 'Please verify your email to log in!')
            logout_then_login(self.request)
        
        self.object = form.save()
        return super().form_valid(form)

    def get_object(self):
        return get_object_or_404(CustomUser, pk=self.request.user.id)

class CustomLoginView(LoginView):
    authentication_form = CustomUserAuthenticationForm
    redirect_authenticated_user = True
    #success_url not needed. There's a LOGIN_REDIRECT_URL in base.py settings.

    # Uncomment this part to log in only verified email users (done for easier testing.)
    # def form_valid(self, form):
    #     user = form.get_user()
    #     if not user.email_verified:
    #         messages.error(self.request, 'Please verify your email to log in!')
    #         return render(self.request, self.template_name, { 'form': self.form_class })

    #     auth_login(self.request, user)
    #     messages.success(self.request, 'Successfully signed in.')
    #     return redirect(self.get_success_url())

class ResendEmailVerificationView(SuccessMessageMixin, FormView):
    template_name = 'registration/resend-email-verification.html'
    success_url = reverse_lazy('users:login')
    form_class = ResendEmailVerificationForm
    #Can't use success_message, cos it attaches to form_valid

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:dashboard')

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        try:
            self.user = CustomUser.objects.get(email__iexact=form['email'].value()) #form.cleaned_data is accessible after running form.is_valid(), which works for non-registered users only.
        except Exception as e:
            self.user = None

        if self.user:
            if self.user.email_verified == False:
                send_verification_email(self.request, self.user)
                messages.success(self.request, 'Email verification resent. Please verify your email to log in.')
                return redirect(self.get_success_url())
            else:
                messages.error(self.request, 'User\'s email already verified!')
        else:
            messages.error(self.request, 'User with this email not found!')

        return render(self.request, self.template_name, { 'form': self.form_class })

class ActivateUserView(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except Exception as e:
            user = None

        if user and generate_token.check_token(user, token):
            user.email_verified = True
            user.save()

            messages.add_message(request, messages.SUCCESS,
                                 'Email verified, you can now login')
            return redirect(reverse_lazy('users:login'))

        messages.add_message(request, messages.ERROR,
                                 'Something went wrong with your link.')
        return render(request, 'registration/activate-fail.html', {"user": user})

# Defining custom classes to successfully reverse django.contrib.auth.urls, 
# since they're in the users' app and use django messages framework
class CustomPasswordResetView(SuccessMessageMixin, PasswordResetView):
    success_url = reverse_lazy("users:password_reset_done")
    success_message = "Password reset email sent. Check your email to reset your password."

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:password_change')

        return super().dispatch(request, *args, **kwargs)

class CustomPasswordResetConfirmView(SuccessMessageMixin ,PasswordResetConfirmView):
    success_url = reverse_lazy("users:login")
    success_message = mark_safe("Your password has been successfully reset.<br/>You can now login with your new password.")

    #Copied from PasswordResetConfirmView, changed the unsuccessful page redirect
    @method_decorator(sensitive_post_parameters())
    @method_decorator(never_cache)
    def dispatch(self, *args, **kwargs):
        if "uidb64" not in kwargs or "token" not in kwargs:
            raise ImproperlyConfigured(
                "The URL path must contain 'uidb64' and 'token' parameters."
            )

        self.validlink = False
        self.user = self.get_user(kwargs["uidb64"])

        if self.user is not None:
            token = kwargs["token"]
            if token == self.reset_url_token:
                session_token = self.request.session.get(INTERNAL_RESET_SESSION_TOKEN)
                if self.token_generator.check_token(self.user, session_token):
                    # If the token is valid, display the password reset form.
                    self.validlink = True
                    return super().dispatch(*args, **kwargs)
            else:
                if self.token_generator.check_token(self.user, token):
                    # Store the token in the session and redirect to the
                    # password reset form at a URL without the token. That
                    # avoids the possibility of leaking the token in the
                    # HTTP Referer header.
                    self.request.session[INTERNAL_RESET_SESSION_TOKEN] = token
                    redirect_url = self.request.path.replace(
                        token, self.reset_url_token
                    )
                    return HttpResponseRedirect(redirect_url)

        # Display the "Password reset unsuccessful" page.
        messages.add_message(self.request, messages.ERROR,
                                 'Something went wrong with your link.')
        return render(self.request, 'registration/reset-fail.html', {"user": self.user})

class CustomPasswordChangeView(SuccessMessageMixin ,PasswordChangeView):
    success_url = reverse_lazy("users:login")
    success_message = mark_safe("Your password has been successfully changed.<br/>You can log in with your new password.")

    def form_valid(self, form):
        form.save()
        # Updating the password logs out all other sessions for the user
        # except the current one.
        update_session_auth_hash(self.request, form.user)
        #Make the user use his new password
        auth_logout(self.request)
        return super().form_valid(form)