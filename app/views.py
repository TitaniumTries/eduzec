from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.list import ListView
from django.views.generic import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db.models import Count

from users.forms import CustomUserCreationForm, CustomUserChangeForm
from users.models import CustomUser
from .models import Answer, Question, Comment

from vote.models import UP, DOWN
from .utilities import cast_vote, save_text_help

class SignUpView(SuccessMessageMixin, CreateView):
    template_name = 'app/register.html'
    success_url = reverse_lazy('login')
    form_class = CustomUserCreationForm
    success_message = "%(username)s, your profile was created successfully!"

class EditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'app/edit_account.html'
    success_url = reverse_lazy('app:edit_account')
    form_class = CustomUserChangeForm
    success_message = "Successfully updated profile!"

    def get_object(self):
        return get_object_or_404(CustomUser, pk=self.request.user.id)

class QuestionsView(ListView):
    model = Question
    template_name = 'app/questions.html'
    context_object_name = "quests"
    paginate_by = 5

    def get_queryset(self):
        qs = super(QuestionsView, self).get_queryset()

        search = self.request.GET.get('q')
        if search:
            qs = qs.filter(title__icontains=search)

        qs = qs.order_by("-id")
        qs = qs.annotate(count_of_answers=Count('answer'))
        return qs

class QuestionDetailView(DetailView):
    model = Question
    template_name = 'app/detail.html'
    context_object_name = 'quest'

    def get_context_data(self, **kwargs):
        context = super(QuestionDetailView, self).get_context_data(**kwargs)

        context['tags'] = self.object.tags.split(',')
        answers = Answer.objects.filter(question=self.object).order_by('-vote_score')    
        comments = []
        for answer in answers:
            comments.append(Comment.objects.filter(answer=answer))
        context['answers_comments'] = zip(answers, comments)
        
        return context

    def get_queryset(self):
        qs = super(QuestionDetailView, self).get_queryset()
        qs = qs.annotate(count_of_answers=Count('answer'))

        return qs

class WriteCommentAnswerView(View):
    def post(self, request):
        text=request.POST['text']
        id=request.POST['id']
        text_type = request.POST['type']
        user=request.user

        if text_type == "comment":
            return render(request, 'includes/single_comment.html', {'comment': save_text_help(text, id, text_type, user)})
        else:
            return render(request, 'includes/single_answer.html', {'answer': save_text_help(text, id, text_type, user)})

class SaveVoteView(LoginRequiredMixin, View):
    def post(self, request):
        id = request.POST['id']
        user_id = request.user.id
        vote_to = request.POST['vote_to']
        vote_type = request.POST['vote_type']

        return JsonResponse({'bool': cast_vote(vote_type, vote_to, user_id, id)})