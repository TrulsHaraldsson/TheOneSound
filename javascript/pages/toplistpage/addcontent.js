$(document).ready(function() {

  $("#submit-toplist-content").click(function() {
    var form = $("#update-content-form");
    var toplist_id = form.data("toplist-id");
    var form_data = form.serialize();
    onCommentSubmit(toplist_id, form_data);
  });

  function onCommentSubmit(toplist_id, form_data){
    $.ajax({
      method: "PUT",
      data: form_data,
      url: "/api/toplists/"+toplist_id, //http://theonesound-148310.appspot.com
      statusCode: {
        401: function(){
          alert("You need to be logged in to do that.");
        },
        404: function(){
        }
      },
      success: function(){
        alert("success!")
      }

    })
  }

})
