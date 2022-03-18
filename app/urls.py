from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name="app/index.html"), name='landing'),
    path('register/', views.SignUpView.as_view(), name='register'),
    path('', include('django.contrib.auth.urls')),
    path('dashboard/', login_required(TemplateView.as_view(template_name="app/dashboard.html")), name='dashboard'),
    path('edit/', views.EditView.as_view(), name='edit_account'),
    path('questions/', views.QuestionsView.as_view(), name='questions'),
    path('detail/<pk>', views.QuestionDetailView.as_view(), name='detail'),
    path('save-text', views.WriteCommentAnswerView.as_view(), name='save-text'),
    path('save-vote', views.SaveVoteView.as_view(), name='save-vote'),
]
