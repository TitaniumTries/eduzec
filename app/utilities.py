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

def save_text_help(text, id, text_type, user_id):
    if text_type == "answer":
        obj = Answer.objects.create(
            question=Question.objects.get(pk=id),
            user=user_id,
            detail=text
        )
    else:
        obj = Comment.objects.create(
            answer=Answer.objects.get(pk=id),
            comment=text,
            user=user_id
        )
    
    return obj