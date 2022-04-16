from django import forms
from django.forms import ModelForm
from .models import Question
from .models import Answer, Question

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'detail', 'tags']
        exclude = ('user', 'add_time')

class AnswerForm(ModelForm):
    class Meta:
        model = Answer
        fields = ['detail']
        exclude = ('user', 'add_time')
