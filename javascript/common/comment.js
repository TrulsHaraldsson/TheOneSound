
$(document).ready(function() {

    $("#comment-form").submit(function() {
        var form = $("#comment-form");
        var commentable_id = form.data("commentable-id");
        var type = form.data("type");
        var comment_text = $("#comment-form").serialize();
        onCommentSubmit(form);
        return false;
    });

    function resetCommentForm($form) {
        /*
        * Will remove the text inside the input:text element that belongs to the given form
        */
        $form.find('textarea[name="comment_text"]').val('');
    }

    function onCommentSubmit(form){
            var commentable_id = form.data("commentable-id");
            var type = form.data("type");
            var comment_text = form.serialize();
            var text = form.find('textarea[name="comment_text"]').val();

            data_string = comment_text;
            $.ajax({
                method: "PUT",
                data: data_string,
                url: "/api/"+type+"/"+commentable_id, //http://theonesound-148310.appspot.com
                statusCode: {
                    401: function(){
                      alert("You need to be logged in to do that.");
                    }
                },
                success: function(){
                    resetCommentForm(form);
                    var commentSection = $("#comment-section") // This is a class panel-body from BS
                    var li = $('<p></p>')
                        .text(text)
                        .prependTo(commentSection)
                }

            })
        }
})
