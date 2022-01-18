from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


def landing(request):
    return render(request, "app/index.html")


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin')
    else:
        form = UserCreationForm()
    return render(request, 'app/signup.html', {'form': form})


def signin(request):
    if request.method == "POST":
        form = AuthenticationForm(data= request.POST)
        if form.is_valid():
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'app/signin.html', {'form': form})

def dashboard(request):
    return render(request, 'app/dashboard.html')
def forum(request):
    return HttpResponse('Hello World! This is the FORUM page!')
