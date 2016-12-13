$(document).ready(function() {

  //addSubmitListener("#update-picture-form", "bands", showNewPicture);
  addSubmitListener("#update-description-form", "bands", showNewDescription);
  addSubmitListener("#update-members-form", "bands", showNewMember);
  addSubmitListener("#update-genres-form", "bands", showNewGenre);
  addSubmitListener("#button-add-album", "bands", nothing);

  addPostSubmitListener("#new-entity-form", "albums")

})
