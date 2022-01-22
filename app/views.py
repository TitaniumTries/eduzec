from django.contrib.auth import logout as dj_auth_logouts
from django.shortcuts import render, redirect

from .forms import UserRegisterForm


def landing(request):
    return render(request, "app/index.html")


def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('../dashboard')
    else:
        form = UserRegisterForm()
    return render(request, 'app/register.html', {'form': form})


def logouts(request):
    if request.method == "POST":
        dj_auth_logouts(request)
    return render(request, 'app/logout.html')


def dashboard(request):
    return render(request, 'app/dashboard.html')
