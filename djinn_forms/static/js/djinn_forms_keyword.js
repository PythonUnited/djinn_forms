/**
 * Keyword widget JS
 */

if (djinn === undefined) {
    var djinn = {};
}


if (djinn.forms === undefined) {
  djinn.forms = {};
}


djinn.forms.keyword = {};


djinn.forms.keyword.appendKw = function(widget, val) {

  var input = widget.find("input[type=hidden]");

  if (djinn.forms.hasValue(input, val, ",")) {
    return false;
  }

  widget.find("ul").append('<li data-value="' + val + '">' + val + '<a href="#" class="delete">&times;</a></li>');
  djinn.forms.addValue(input, val, true, ",");

  if (widget.find("li").length >= parseInt(widget.data("maxkeywords"))) {
    widget.find(".new_kw").hide();
  }
};


djinn.forms.keyword.select = function(e, ui) {

  var value =  ui.item.value;
  var widget = $(e.target).parents(".keyword");
  var input = widget.find(".new_kw");

  djinn.forms.keyword.appendKw(widget, value);

  input.val("");
};


$.fn.forms_keywords_initializer = function(){

  $(".new_kw").each(function() {

    var input = $(this);
    var hidden = input.parents(".keyword").find("input[type=hidden]");


    if (input.parent().find("li").length >= parseInt(input.parent().data("maxkeywords"))) {
      input.parent().find(".new_kw").hide();
    }

    input.autocomplete({
      source: input.data("search_url"),
      minLength: input.data("search_minlength"),
      select: djinn.forms.keyword.select,
      focus: function(e, ui) {
        e.preventDefault();
      },
      response: function(e, ui) {
        
        var content = ui.content.slice(0);
        content.reverse();

        $.each(content, function(idx, obj) {

          if (djinn.forms.hasValue(hidden, obj.value, ",")) {
            ui.content.splice(idx, 1);
          } 
        });
      }
    });
  });

  $(document).on("click", ".keyword ul", function(e) {

    $(e.currentTarget).find("input").focus();
  });

  $(document).on("keydown", ".new_kw", function(e) {

    var input = $(e.currentTarget);
    var widget = input.parents(".keyword");
    // 13 = enter, 32 = space, 188 = comma

    if (e.keyCode == 13 || e.keyCode == 188) {
      // enter and comma not in keywords
      e.preventDefault();

      // finish the current keyword and add it as 'button'
      djinn.forms.keyword.appendKw(widget, $(e.currentTarget).val());

      // empty the keyword-input box
      input.val("");
    }
  });

  $(document).on("click", ".keyword .delete", function(e) {

    e.preventDefault();

    var widget = $(e.currentTarget).parents(".keyword");
    var input = widget.find("input[type=hidden]");

    var elt = $(e.currentTarget).parents("li");

    djinn.forms.removeValue(input, elt.data('value'), ",");

    elt.remove();

    if (widget.find("li").length < parseInt(widget.data("maxkeywords"))) {
      widget.find(".new_kw").show();
    }

  });
}

$(document).ready(function() {
    $.fn.forms_keywords_initializer();
});


