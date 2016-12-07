$(document).ready(function(){
  $.ajax({
    method: get,
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
})

function displayBandInfo(data){
  //display the gathered info on bandpage/display
}
