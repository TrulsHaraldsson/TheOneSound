$(document).ready(function() {

  addSubmitListener("#update-picture-form", "albums");
  addSubmitListener("#update-description-form", "albums");
  addPostSubmitListener("#new-entity-form", "tracks")


  $("#button-add-entity").click(function(){
    $("#div-add-entity").toggle();
  });
})
