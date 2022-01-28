from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect

from .forms import UserRegisterForm, EditProfileForm


def landing(request):
    return render(request, "app/index.html")


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'app/register.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'app/dashboard.html')


@login_required
def edit(request):
    if request.method == "POST":
        form = EditProfileForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(request, "Error updating your profile. Check the form below.")
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, "app/edit_account.html", {"form": form})
