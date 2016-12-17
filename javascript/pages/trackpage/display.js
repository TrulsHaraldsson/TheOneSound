$(document).ready(function() {

  addSubmitListener("#update-youtube-form", "tracks", showNewYoutubeVideo);
  addSubmitListener("#update-description-form", "tracks", showNewDescription);

  $("#toggle-description").click(function (){
    $("#description-edit").toggle();
    $("#description-display").toggle();
  });

  $("#toggle-youtube").click(function (){
    $("#youtube-edit").toggle();
  });

})
