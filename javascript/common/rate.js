$(document).ready(function() {

    $("#like").click(function() {
        console.log("like clicked");
        var rated = $("#rating-div").data("rated");
        console.log(rated);
        if (rated == "None") {
            onRatingSubmit("1");
            $("#rating-div").data("rated", "True");
            updateHTML("#likes", 1);
        }
        else if (rated == "False") {
          onRatingSubmit("1");
          $("#rating-div").data("rated", "True");
          updateHTML("#likes", 1);
          updateHTML("#dislikes", -1);
        }
    });

    $("#dislike").click(function() {
      var rated = $("#rating-div").data("rated");
      if (rated == "None" ) {
          onRatingSubmit("0");
          $("#rating-div").data("rated", "False");
          updateHTML("#dislikes", 1);
      }
      else if (rated == "True") {
        onRatingSubmit("0");
        $("#rating-div").data("rated", "False");
        updateHTML("#likes", -1);
        updateHTML("#dislikes", 1);
      }
    });

    function updateHTML(id, amount){
      var newVal = parseInt($(id).html(), 10) + amount;
      $(id).html(newVal);
    }


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
