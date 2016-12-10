
$(document).ready(function() {

    $("#comment-form").submit(function() {
        var form = $("#comment-form");
        var commentable_id = form.data("commentable-id");
        var type = form.data("type");
        var comment_text = $("#comment-form").serialize();
        //onCommentSubmit(commentable_id, comment_text, type);
        onCommentSubmit(form)
        resetCommentForm(form)
        return false;
    });

    function resetCommentForm($form) {
        /*
        * Will remove the text inside the input:text element that belongs to the given form
        */
        $form.find('input:text').val('');
    }

    function onCommentSubmit(form){
            var commentable_id = form.data("commentable-id");
            var type = form.data("type");
            var comment_text = form.serialize();
            var text = form.find('input:text').val()

            data_string = comment_text;
            $.ajax({
                method: "PUT",
                data: data_string,
                url: "/api/"+type+"/"+commentable_id, //http://theonesound-148310.appspot.com
                statusCode: {
                    404: function(){
                    }
                },
                success: function(){
                    var commentSection = $("#comment-section") // This is a class panel-body from BS
                    var li = $('<p></p>')
                        .text(text)
                        .prependTo(commentSection)
                }

            })
        }
})
