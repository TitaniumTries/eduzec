from django.http.response import HttpResponse
from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
def home(request):
    return HttpResponse('Hello World! This is the LANDING page!')
def signup(request):
    return HttpResponse('Hello World! This is the SIGNUP page!')
def login(request):
    return HttpResponse('Hello World! This is the LOGIN page!')
def forum(request):
    return HttpResponse('Hello World! This is the FORUM page!')