
$(document).ready(function() {

  $("#submit-comment").click(function() {
    var form = $("#comment-form");
    var band_id = form.data("band-id");
    var user_id = form.data("user-id");
    var comment_text = $("#comment-form").serialize();
    onCommentSubmit(band_id, comment_text, user_id);
  });

  function onCommentSubmit(band_id, comment_text, user_id){
    json_data = JSON.stringify({"comment_text": comment_text,
                  "user_id": user_id});
    data_string = comment_text+"&"+
                  "user_id="+user_id;
    $.ajax({
      method: "PUT",
      data: data_string,
      url: "/api/band/"+band_id, //http://theonesound-148310.appspot.com
      statusCode: {
        404: function(){
          alert("page not found!");
        }
      },
      success: function(){
        alert("success!!");
      }

    })
  }

})
