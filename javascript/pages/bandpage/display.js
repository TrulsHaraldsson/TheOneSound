$(document).ready(function() {

  addSubmitListener("#update-picture-form", "bands");
  addSubmitListener("#update-biography-form", "bands");
  addSubmitListener("#update-members-form", "bands");
  addSubmitListener("#update-genres-form", "bands");
  /*
  function addSubmitListener(form_id){
    $(form_id).submit(function() {
      var form = $(form_id);
      var id = form.data("id");
      var form_data = form.serialize();
      onBandUpdate(form_data, id);
      return false;
    });
  }

  function onBandUpdate(form_data, id){
    $.ajax({
      method: "PUT",
      data: form_data,
      url: "/api/bands/"+id, //http://theonesound-148310.appspot.com
      statusCode: {
        404: function(){
          alert("something wrong!");
        }
      },
      success: function(){
        console.log("put ok!");
      }
    })
  }*/

})
