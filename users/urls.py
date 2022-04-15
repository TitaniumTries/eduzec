from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('register/', views.SignUpView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('', include('django.contrib.auth.urls')),
    path('dashboard/', login_required(TemplateView.as_view(template_name="users/dashboard.html")), name='dashboard'),
    path('edit/', views.EditView.as_view(), name='edit_account'),
    path('activate-user/<uidb64>/<token>',
         views.activate_user, name='activate'),
]