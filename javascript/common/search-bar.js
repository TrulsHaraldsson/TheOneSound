$(document).ready(function() {

  $("#search-bar").click(function() {
    var form = $("#comment-form");
    var name = form.serialize();
    var url = "/api/bands?name="+name;
    var bands = onSearchSubmit(url);
    var url = "/api/albums?name="+name;
    var albums = onSearchSubmit(url);
    var url = "/api/tracks?name="+name;
    var tracks = onSearchSubmit(url);

  });

  function onSearchSubmit(url){
    $.ajax({
      method: "GET",
      data: data_string,
      url: url, //http://theonesound-148310.appspot.com
      statusCode: {
        404: function(){
          alert("page not found!");
        }
      },
      success: function(){
        alert("success!!");
      }

    })

  }

})
