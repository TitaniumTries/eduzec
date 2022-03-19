from django.urls import path
from . import views

urlpatterns = [
    path('questions/', views.QuestionsView.as_view(), name='questions'),
    path('detail/<pk>', views.QuestionDetailView.as_view(), name='detail'),
    path('save-text', views.WriteCommentAnswerView.as_view(), name='save-text'),
    path('save-vote', views.SaveVoteView.as_view(), name='save-vote'),
]
