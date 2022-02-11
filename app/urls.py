from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/', views.edit, name='edit_account'),
    path('questions/', views.questions, name='questions'),
]
