from django.conf import settings
from django.db import models
from vote.models import VoteModel

from users.models import CustomUser


# This is the question model
class Question(VoteModel, models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    detail = models.TextField()
    tags = models.TextField(default='')
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# This is the answer model

class Answer(VoteModel, models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    detail = models.TextField()
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.detail


class Comment(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comment_user')
    comment = models.TextField(default='')
    add_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on \"{self.answer}\" by {self.user}"