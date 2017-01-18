$(document).ready(function() {

  setListeners();

  function setListeners(){
    $("#toplist-list li").each(function(){
      if ($(this).data("toplist-id") != "None") {
        $(this).click(function(){
          var toplist_id = $(this).data("toplist-id");
          console.log(toplist_id);
          var content_id = $(this).data("content-id");
          console.log(content_id);
          var data = "content_id="+content_id;
          onAdd(toplist_id, data);
        });
      }

    });

  }



  function onAdd(toplist_id, data){
    $.ajax({
      method: "PUT",
      data: data,
      url: "/api/toplists/"+toplist_id, //http://theonesound-148310.appspot.com
      statusCode: {
        401: function(){
          alert("You need to be logged in to do that.");
        },
        404: function(){
          alert("Something went wrong!");
        }
      },
      success: function(){
        console.log("Success!");
      }

    });
  }


})
