from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views
from django.views.generic import TemplateView
from django.contrib.auth.views import PasswordResetDoneView, PasswordResetCompleteView

urlpatterns = [
    path('register/', views.SignUpView.as_view(), name='register'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path("password_change/", views.CustomPasswordChangeView.as_view(), name="password_change"),
    path("password_reset/", views.CustomPasswordResetView.as_view(), name="password_reset"),
    path("reset/<uidb64>/<token>/", views.CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('', include('django.contrib.auth.urls')),
    path('dashboard/', login_required(TemplateView.as_view(template_name="users/dashboard.html")), name='dashboard'),
    path('edit/', views.EditView.as_view(), name='edit_account'),
    path('activate-user/<uidb64>/<token>',
         views.ActivateUserView.as_view(), name='activate'),
    path('resend/', views.ResendEmailVerificationView.as_view(), name='resend_email')
]