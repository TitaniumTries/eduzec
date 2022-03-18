$(document).ready(function(){
    $('.cast-vote').on('click',function(){
        var _vote_type=$(this).closest('[vote_type]').attr('vote_type');
        var _id = $(this).closest('[id]').attr('id');
        var _vote_to=$(this).closest('[vote_to]').attr('vote_to');
        // Ajax starts here i guess
        $.ajax({
            url:'/save-vote',
            type:'post',
            data:{
                vote_type:_vote_type,
                vote_to:_vote_to,
                id:_id,
                csrfmiddlewaretoken:csrf_token,
            },
            dataType:'json',
            beforeSend:function(){

            },
            success:function(res){
                if(res.bool==true){
                    if (_vote_to == "question")
                        obj = "question"
                    else
                        obj = "answer"
                    votes = parseInt($('.voting[id=' + _id + ']').find('.' + obj + '_votes').text())
                    if (_vote_type == "upvote")
                        $('.voting[id=' + _id + ']').find('.' + obj + '_votes').html(votes + 1)
                    else
                        $('.voting[id=' + _id + ']').find('.' + obj + '_votes').html(votes - 1)
                }
            }
        });
    });
});


$(document).ready(function(){
    $('.save-text-btn').on('click',function(){
        var _id=$(this).data('id');
        var _text=$(this).siblings('.save-text').val();
        var _type=$(this).closest('[text_type]').attr('text_type');
        // Ajax starts here i guess
        $.ajax({
            url:'/save-text',
            type:'post',
            data:{
                text:_text,
                id:_id,
                type:_type,
                csrfmiddlewaretoken:csrf_token,
            },
            beforeSend:function(){
                $('.save-text-btn[data-id=' + _id + ']').addClass('disabled').text('saving...');
            },
            success:function(data){
                $('.save-text-btn[data-id=' + _id + ']').siblings('.save-text').val('');
                if (_type == "comment") {
                    $('.comment-wrapper[id=' + _id + ']').prepend(data);
                }
                else {
                    $('.write-answer').after(data);
                }

                if (_type == "comment") {
                    obj = "Comment";
                }
                else {
                    obj = "Answer";
                }

                $('.save-text-btn[data-id=' + _id + ']').removeClass('disabled').text(obj);
            }
        });
    });
});
