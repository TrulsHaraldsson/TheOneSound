function addSubmitListener(form_id, type){
  $(form_id).submit(function() {
    var form = $(form_id);
    var id = form.data("id");
    var form_data = form.serialize();
    onEntityUpdate(form_data, id, type);
    return false;
  });
}

function onEntityUpdate(form_data, id, type){
  $.ajax({
    method: "PUT",
    data: form_data,
    url: "/api/" + type + "/"+id, //http://theonesound-148310.appspot.com
    statusCode: {
      404: function(){
        alert("something wrong!");
      }
    },
    success: function(){
      console.log("put ok!");
      successFunction();
    }
  })
}


function showNewDescription() {
  var newText = $("#description-textarea").val();
  $("#description-display").text(newText);
  $("#description-edit").toggle();
  $("#description-display").toggle();
}

function showNewYoutubeVideo() {
  var newLink = $("#youtube-input").val();
  $("#youtube-vid").attr('src', newLink);
  $("#youtube-edit").toggle();
}
