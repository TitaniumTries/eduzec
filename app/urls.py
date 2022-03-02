from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('register/', views.register, name='register'),
    path('', include('django.contrib.auth.urls')),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/', views.edit, name='edit_account'),
    path('questions/', views.questions, name='questions'),
    path('detail/<int:id_>', views.detail, name='detail'),
    path('save-comment', views.save_comment, name='save-comment'),
]
