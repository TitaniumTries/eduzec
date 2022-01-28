from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import UserRegisterForm


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
