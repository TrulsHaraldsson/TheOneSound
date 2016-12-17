$(document).ready(function() {
  addPostSubmitListener("#create-toplist-form", "toplists");
  $("#button-add-toplist").click(function (){
    $("#div-add-toplist").toggle();
  });
})
