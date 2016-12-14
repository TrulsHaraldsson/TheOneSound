$(document).ready(function(){

    $("#update-picture-form").submit(function() {
      var form = $("#update-picture-form");
      var id = form.data("id");
      var type = form.data("type");
      var file = document.getElementById("file-input").files[0];
      var formData = new FormData();
      console.log(file.name+" size: "+file.size);
      formData.append("image", file);
      formData.append("id", id);
      formData.append("type", type);

      onPictureUpload(formData, id, type, file);
      return false;
    })


  function onPictureUpload(formData, id, type, file){
    $.ajax({
      method: "POST",
      data: formData,
      processData: false,  // tell jQuery not to process the data
      contentType: false,  // tell jQuery not to set contentType
      url: "/api/storage", //http://theonesound-148310.appspot.com
      statusCode: {
        404: function(){
          alert("something wrong!");
        }
      },
      success: function(){
        console.log("post ok!");
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#img-default')
                .attr('src', e.target.result);
            $('#img-element')
                .attr('src', e.target.result);
        };
        reader.readAsDataURL(file);
        //var d = new Date();
        //var src = $("#img-element").attr("src");
        //$("#img-element").attr("src", src + "?" + d.getTime());
        //console.log("picture updated!");
        //var formData = new FormData();
        //formData.append("picture_url", "https://storage.googleapis.com/theonesound-148310.appspot.com/" + type + "/" + id);
        //onEntityUpdate(formData, id, type, showNewPicture);
      }
    })
  }
})
