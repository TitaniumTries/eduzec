from .models import Answer, Question, Comment
from vote.models import UP, DOWN

def cast_vote(vote_type, vote_to, user_id, id):
    success = True

    if vote_to == "question":
        obj = Question.objects.get(pk=id)
    else:
        obj = Answer.objects.get(pk=id)

    if vote_type == "upvote":
        if obj.votes.exists(user_id):
            success = False
        else:
            obj.votes.up(user_id)
    else:
        if obj.votes.exists(user_id, action=DOWN):
            success = False
        else:
            obj.votes.down(user_id)
    return success

