from django.forms import ModelForm
from .models import Question

class QuestionForm(ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'detail', 'tags']
        exclude = ('user', 'add_time')
