$(document).ready(function() {

  $("#submit-new-toplist").click(function() {
    var form = $("#new-toplist-form");
    var form_data = form.serialize();
    onToplistSubmit(form_data);
  });

  function onToplistSubmit(form_data){
    $.ajax({
      method: "POST",
      data: form_data,
      dataType: 'json',
      url: "/api/toplists", //http://theonesound-148310.appspot.com
      statusCode: {
        404: function(){
        }
      },
      success: function(data){
        window.location.replace("/toplistpage/" + data.id);
      }
    })
  }

})
