
$(document).ready(function() {

  $("#submit-comment").click(function() {
    var form = $("#comment-form");
    var commentable_id = form.data("commentable-id");
    var type = form.data("type");
    var comment_text = $("#comment-form").serialize();
    onCommentSubmit(commentable_id, comment_text, type);
  });

  function onCommentSubmit(commentable_id, comment_text, type){
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
      }

    })
  }

})
