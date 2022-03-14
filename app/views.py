import json
from pickle import FALSE
from xml.etree.ElementTree import Comment

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import JsonResponse

from users.forms import CustomUserCreationForm, CustomUserChangeForm
from .models import Answer, Question, Comment

from vote.models import UP, DOWN
from .utilities import cast_vote, save_text_help

def landing(request):
    return render(request, "app/index.html")


def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:login')
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
    quests = paginator.page(page_num)
    return render(request, 'app/questions.html', {'quests': quests})


def detail(request, id_):
    quest = Question.objects.get(pk=id_)
    tags = quest.tags.split(',')
    answers = Answer.objects.filter(question=quest).order_by('-vote_score')
    comments = []
    for answer in answers:
        comments.append(Comment.objects.filter(answer=answer))
    answers_comments = zip(answers, comments)
    num_answers = len(answers)
    return render(request, 'app/detail.html', {'quest': quest, 'tags': tags, 'answers_comments': answers_comments, 'num_answers': num_answers})

def save_text(request):
    if request.method=='POST':
        text=request.POST['text']
        id=request.POST['id']
        text_type = request.POST['type']
        user=request.user

        return JsonResponse({'bool': save_text_help(text, id, text_type, user)})

def save_vote(request):
    if request.method=='POST':
        id = request.POST['id']
        user_id = request.user.id
        vote_to = request.POST['vote_to']
        vote_type = request.POST['vote_type']

        return JsonResponse({'bool': cast_vote(vote_type, vote_to, user_id, id)})