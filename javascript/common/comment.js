
$(document).ready(function() {

  $("#submit-comment").click(function() {
    var form = $("#comment-form");
    var commentable_id = form.data("commentable-id");
    var user_id = form.data("user-id");
    var type = form.data("type");
    var comment_text = $("#comment-form").serialize();
    onCommentSubmit(commentable_id, comment_text, user_id, type);
  });

  function onCommentSubmit(commentable_id, comment_text, user_id, type){
    json_data = JSON.stringify({"comment_text": comment_text,
                  "user_id": user_id});
    data_string = comment_text+"&"+
                  "user_id="+user_id;
    $.ajax({
      method: "PUT",
      data: data_string,
      url: "/api/"+type+"/"+commentable_id, //http://theonesound-148310.appspot.com
      statusCode: {
        404: function(){
        }
      },
      success: function(){
      }

    })
  }

})
