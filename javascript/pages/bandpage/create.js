$(document).ready(function() {

  $("#new-band-form").submit(function() {
    var form = $("#new-band-form");
    var form_data = form.serialize();
    onBandSubmit(form_data);
    return false;
  });

  function onBandSubmit(form_data){
    $.ajax({
      method: "POST",
      data: form_data,
      dataType: 'json',
      url: "/api/bands", //http://theonesound-148310.appspot.com
      statusCode: {
        404: function(){
          alert("something wrong!");
        }
      },
      success: function(data){
        window.location.replace("/bandpage/" + data.id);
      }
    })
  }

})
