from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from . forms import UserRegisterForm
from django.contrib.auth import logout as logouts


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
        logouts(request)
    return render(request, 'app/logout.html')


def dashboard(request):
    return render(request, 'app/dashboard.html')



