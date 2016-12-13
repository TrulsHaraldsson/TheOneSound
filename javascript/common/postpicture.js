$(document).ready(function(){

    $("#update-picture-form").submit(function() {
      var form = $(this);
      var id = form.data("id");
      var type = form.data("type");
      var form_data = form.serialize();
      form_data += "&id="+id+"&type="+type;
      onEntityUpdate(form_data, id, type);
      return false;
    }


  function onEntityUpdate(form_data, id, type){
    $.ajax({
      method: "POST",
      data: form_data,
      url: "/api/storage", //http://theonesound-148310.appspot.com
      statusCode: {
        404: function(){
          alert("something wrong!");
        }
      },
      success: function(){
        console.log("post ok!");
      }
    })
  }
})
