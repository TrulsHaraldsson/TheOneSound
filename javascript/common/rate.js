$(document).ready(function() {

    $("#like").click(function() {
        onRatingSubmit("1");
    });

    $("#dislike").click(function() {
        onRatingSubmit("0");
    });

    function onRatingSubmit(rating){
      var div = $("#rating-div");
      var type = div.data("type");
      var id = div.data("id");
      data_string = "rating="+rating;
      $.ajax({
            method: "PUT",
            data: data_string,
            url: "/api/"+type+"/"+id, //http://theonesound-148310.appspot.com
            statusCode: {
                  404: function(){
                  }
            },
              success: function(){
            }

      })
    }

})
