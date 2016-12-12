$(document).ready(function() {

  addSubmitListener("#update-youtube-form", "tracks");
  addSubmitListener("#update-description-form", "tracks");

  $("#toggle-description").click(function (){
    $("#description-edit").toggle();
    $("#description-display").toggle();
  });

})
