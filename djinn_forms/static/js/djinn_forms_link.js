/**
 * Link widget JS
 */

$(document).ready(function() {

  $(document).on("click", ".link a", function(e) {

    e.preventDefault();

    var link = $(e.currentTarget);

    $.get(link.attr("href"), function(data) {

      djinn.contenttypes.show_modal(data);
    });

  });
  
});