var $ = jQuery;
$(document).ready(function(){
  $("#tag-search").on("keyup", function() {
    var value = $(this).val().toLowerCase();
    $("#tag dt").filter(function() {
      $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
    });
  });
});