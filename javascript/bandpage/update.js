function onFormSubmit(){

  $.ajax({
    method: post,
    dataType: json,
    data: "jsonObject",
    url: "blabla",
    statusCode: {
      404: function(){
        alert("page not found!");
      }
    },
    success: displayBandInfo

  })
}

$("#update-form").submit(function( event ) {
  alert( "Handler for .submit() called." );
  event.preventDefault();
});
