from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from users.forms import CustomUserCreationForm, CustomUserChangeForm, CustomUserAuthenticationForm
from .models import Question
from django.core.paginator import Paginator

def landing(request):
    return render(request, "app/index.html")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'app/register.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'app/dashboard.html')


@login_required
def edit(request):
    if request.method == "POST":
        form = CustomUserChangeForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully")
        else:
            messages.error(request, "Error updating your profile. Check the form below.")
    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, "app/edit_account.html", {"form": form})

def questions(request):
    if 'q' in request.GET:
        q = request.GET['q']
        quests = Question.objects.filter(title__icontains=q).order_by('-id')
    else:
        quests = Question.objects.all().order_by('-id')
    paginator = Paginator(quests, 5)
    page_num = request.GET.get('page', 1)
    quests=paginator.page(page_num)
    return render(request, 'app/questions.html', {'quests': quests})

def detail(request,id):
    quest=Question.objects.get(pk=id)
    return render(request,'app/detail.html', {'quest': quest})

