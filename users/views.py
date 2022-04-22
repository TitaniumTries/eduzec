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
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from .utilities import generate_token, send_verification_email

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