function addPostSubmitListener(form_id, type){
  $(form_id).submit(function() {
    var form = $(form_id);
    var parent_id = form.data("id");
    var form_data = form.serialize();
    onEntityCreate(form_data, parent_id, type);
    return false;
  });
}

function onEntityCreate(form_data, parent_id, type){
  $.ajax({
    method: "POST",
    data: form_data + "&parent_id="+parent_id,
    dataType: 'json',
    url: "/api/"+type, //http://theonesound-148310.appspot.com
    statusCode: {
      401: function(){
        alert("You need to be logged in to do that.");
      },
      404: function(){
        alert("Nothing found!");
      }
    },
    success: function(data){
      window.location.replace("/" + type + "/" + data.id);
    }
  })
}
