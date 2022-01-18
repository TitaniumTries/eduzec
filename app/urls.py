from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='landing'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.login, name='signin'),
    path('forum/', views.forum, name='forum')
]
