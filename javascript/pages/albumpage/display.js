$(document).ready(function() {
  addSubmitListener("#update-description-form", "albums", showNewDescription);
  addPostSubmitListener("#new-entity-form", "tracks")
})
