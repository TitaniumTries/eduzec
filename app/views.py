from django.http import HttpResponse


from django.shortcuts import render


def home(request):
    return render(request, "app/index.html")


def signup(request):
    return HttpResponse('Hello World! This is the SIGNUP page!')


def login(request):
    return HttpResponse('Hello World! This is the LOGIN page!')


def forum(request):
    return HttpResponse('Hello World! This is the FORUM page!')
