$(document).ready(function() {
  /*
  should be for updating profile stuff.
  addSubmitListener("#update-youtube-form", "tracks", showNewYoutubeVideo);
  addSubmitListener("#update-description-form", "tracks", showNewDescription);
  */

  addPostSubmitListener("#create-toplist-form", "toplists");

  $("#button-add-toplist").click(function (){
    $("#div-add-toplist").toggle();
  });
})
