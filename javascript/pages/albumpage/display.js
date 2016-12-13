$(document).ready(function() {

  //addSubmitListener("#update-picture-form", "albums", showNewPicture);
  addSubmitListener("#update-description-form", "albums", showNewDescription);
  addPostSubmitListener("#new-entity-form", "tracks")


  $("#button-add-entity").click(function(){
    $("#div-add-entity").toggle();
  });
})
