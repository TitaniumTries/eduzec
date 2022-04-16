from django.urls import path
from . import views

urlpatterns = [
    path('questions/', views.QuestionsView.as_view(), name='questions'),
    path('ask/', views.AskForm.as_view(), name='ask'),
    path('detail/<pk>', views.QuestionDetailView.as_view(), name='detail'),
    path('answer/', views.AnswerForm.as_view(), name='answer'),
    path('answer/<pk>', views.AnswerForm.as_view(), name='answer_with_pk'),
    path('question/<pk>', views.QuestionDetailView.as_view(), name='detail'),
    path('save-text', views.WriteCommentAnswerView.as_view(), name='save-text'),
    path('save-vote', views.SaveVoteView.as_view(), name='save-vote'),
]