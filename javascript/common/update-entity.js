function addSubmitListener(form_id, type, successFunction){
  $(form_id).submit(function() {
    var form = $(form_id);
    var id = form.data("id");
    var form_data = form.serialize();
    onEntityUpdate(form_data, id, type, successFunction);
    return false;
  });
}

function onEntityUpdate(form_data, id, type, successFunction){
  $.ajax({
    method: "PUT",
    data: form_data,
    url: "/api/" + type + "/"+id, //http://theonesound-148310.appspot.com
    statusCode: {
      401: function(){
        alert("You need to be logged in to do that.");
      },
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
  console.log(newText);
  $("#description-display").text(newText);
  $("#description-edit").collapse("hide");
}

function showNewYoutubeVideo() {
  var newLink = $("#youtube-input").val();
  $("#youtube-vid").attr('src', newLink);
  $("#youtube-edit").toggle();
}

function showNewPicture() {
  var newLink = $("#picture-input").val();
  $("#img-element").attr('src', newLink);
  $("#picture-edit").toggle();
}

function showNewMember() {
  var newText = $("#member-input").val();
  var li = $('<p></p>')
      .text(newText)
      .appendTo($("#members-display"));
}

function showNewGenre() {
  var newText = $("#genre-input").val();
  console.log(newText);
  var li = $('<p></p>')
      .text(newText)
      .appendTo($("#genres-display"));
}

function nothing() {

}
