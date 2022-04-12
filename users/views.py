from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView, UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect

from users.forms import CustomUserCreationForm, CustomUserChangeForm, CustomUserAuthenticationForm
from django.contrib.auth.views import LoginView
from users.models import CustomUser

class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'registration/register.html'
    success_url = reverse_lazy('users:login')
    form_class = CustomUserCreationForm
    success_message = "%(username)s, your profile was created successfully!"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('users:dashboard')

        return super().dispatch(request, *args, **kwargs)

class EditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'users/edit_account.html'
    success_url = reverse_lazy('users:edit_account')
    form_class = CustomUserChangeForm
    success_message = "Successfully updated profile!"

    def get_object(self):
        return get_object_or_404(CustomUser, pk=self.request.user.id)

class CustomLoginView(LoginView):
    authentication_form = CustomUserAuthenticationForm
    redirect_authenticated_user = True
