$(document).ready(function() {

  addSubmitListener("#update-picture-form", "bands", showNewPicture);
  addSubmitListener("#update-biography-form", "bands", nothing);
  addSubmitListener("#update-members-form", "bands", showNewMember);
  addSubmitListener("#update-genres-form", "bands", showNewGenre);
  addSubmitListener("#button-add-album", "bands", nothing);

  addPostSubmitListener("#new-entity-form", "albums")




  $("#toggle-description").click(function (){
    $("#description-edit").toggle();
    $("#description-display").toggle();
  });

  $("#button-add-entity").click(function(){
    $("#div-add-entity").toggle();
  });

  $("#toggle-picture-edit").click(function() {
    $("#picture-edit").toggle();
  })

  $("#toggle-members-edit").click(function() {
    $("#members-edit").toggle();
  })



})
