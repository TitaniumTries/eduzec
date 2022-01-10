from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='landing'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('forum/', views.forum, name='forum')
]
