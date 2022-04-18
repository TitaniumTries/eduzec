import re
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render

from users.forms import CustomUserCreationForm, CustomUserChangeForm, CustomUserAuthenticationForm
from django.contrib.auth.views import LoginView
from users.models import CustomUser

from django.contrib.auth import login as auth_login
from django.contrib.auth.views import logout_then_login
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from .utilities import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_verification_email(request, user):
    current_site = get_current_site(request)
    email_subject = 'Activate your account'
    email_body = render_to_string('registration/activate.html', {
        'user': user,
        'domain': current_site,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': generate_token.make_token(user)
    })

    email = EmailMessage(subject=email_subject, body=email_body,
                         from_email=settings.EMAIL_FROM_USER,
                         to=[user.email]
                         )

    if not settings.TESTING: # Removing this line would not send emails in tests, since Django overrides the specified email client to its default one to prevent this behavior in test. This can be overriden.
        EmailThread(email).start()

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
    #success_url = reverse_lazy('users:dashboard')

    def form_valid(self, form):
        """
        Check that user signup is allowed before even bothering to
        dispatch or do other processing.

        """
        """Security check complete. Log the user in."""
        user = form.get_user()
        if not user.email_verified:
            messages.error(self.request, 'Please verify your email to log in!')
            return render(self.request, self.template_name, { 'form': self.form_class })


        auth_login(self.request, user)
        messages.success(self.request, 'Successfully signed in.')
        return redirect(self.get_success_url())

def activate_user(request, uidb64, token):
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