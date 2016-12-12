$(document).ready(function() {

  addSubmitListener("#update-picture-form", "bands");
  addSubmitListener("#update-biography-form", "bands");
  addSubmitListener("#update-members-form", "bands");
  addSubmitListener("#update-genres-form", "bands");
  addSubmitListener("#button-add-album", "bands");
  addPostSubmitListener("#new-entity-form", "albums")


  $("#toggle-description").click(function (){
    $("#description-edit").toggle();
    $("#description-display").toggle();
  });

  $("#button-add-album").click(function(){
    $("#div-add-album").toggle();
  });

})
