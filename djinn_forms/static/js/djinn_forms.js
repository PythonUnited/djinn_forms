/**
 * Djinn forms JS lib. Mainly helper functions for form widget handling.
 */

if (djinn == undefined) {
    var djinn = {};
}


djinn.forms = {};


/**
 * Given an input, remove the value from the list of values. Assumes
 * that the input contains multiple values separated by <separator>.
 * @param input Input element (jQuery object)
 * @param value Value to remove
 * @param separator Value separator, defaults to ';;'
 */
djinn.forms.removeValue = function(input, value, separator) {

  var new_values = [];
  var old_values = input.val() || "";
  var sep = (separator || ";;");

  old_values = old_values.split(sep);

  for (var i = 0; i < old_values.length; i++) {

    if (old_values[i] != value) {
      new_values.push(old_values[i]);
    }
  }
  input.val(new_values.join(sep));
};


/**
 * Add value to ';;' separated values list.
 * @param input Input element (jQuery object)
 * @param value Value to add
 * @param separator Value separator, defaults to ';;'
 */
djinn.forms.addValue = function(input, value, unique, separator) {

  var sep = (separator || ";;");

  if (!input.val()) {
    input.val(value);
  } else {
    if (!unique) {
      input.val(input.val() + sep + value);
    } else {
      var new_values = [];
      var old_values = input.val();
      
      old_values = old_values.split(sep);
      
      for (var i = 0; i < old_values.length; i++) {
        
        if (old_values[i] != value) {
          new_values.push(old_values[i]);
        }
      }
      new_values.push(value);

      input.val(new_values.join(sep));
    }
  }
};


/**
 * Set link data to widget input.
 */
djinn.forms.set_link = function(url, content_type, obj_id, title, extra_args) {

  var val = url + "::" + content_type + "::" + obj_id;
  val += "::" + (extra_args['target'] || "");

  $("#id_" + extra_args['tgt']).val(val);
  $("#" + extra_args['tgt'] + "_link").html(title || url);

  $("#MyModal").modal("hide");
};


/**
 * Initialize file uploader widget.
 */
djinn.forms.init_fileuploader = function(options) {

  var defaults = {
    url: '/fileupload',
    dataType: 'json',
    done: function (e, data) {
      
      var valuetgt = $($(e.target).data("valuefield"));
      var tgt = $(e.target);
      
      if (tgt.attr("multiple")) {
        $(tgt.data("target")).append(data.result.html);        
        valuetgt.val(valuetgt.val() + "," + data.result.attachment_ids.join(","));
      } else {
        $(tgt.data("target")).html(data.result.html);
        valuetgt.val(data.result.attachment_ids.join(","));
      }
      $(tgt.data("progress") + " .bar").css("width", "100%");

      if (tgt.data("callback")) {
        
        var callback = eval(tgt.data("callback"));
        callback.apply(null, tgt);
      }

      $(document).triggerHandler("djinn_forms_fileupload_done", [e.target, data.result]);
    },
    send: function(e, data) {
      $(document).triggerHandler("djinn_forms_fileupload_send", [e.target]);
    },
    progress: function (e, data) {
      var progress = parseInt(data.loaded / data.total * 100, 10);
      $($(e.target).data("progress") + " .bar").css("width", progress + "%");
    }
  };
  
  if (options) {
    $.extend(defaults, options);
  }
  
  $("input[type='file']").each(function() {
      
      if ($(this).data("uploadurl")) {
        defaults['url'] = $(this).data("uploadurl");
      }
      defaults['dropZone'] = $(this).attr("id");

      defaults['formData'] = {
        "attachment_id": $(this).hasClass("field") ? $($(this).data("valuefield")).val() : "",
        "attachment_type": $(this).data("attachmenttype"),
        "edit_type": $(this).hasClass("field") ? "field": "attachment"
      }
      
      $(this).fileupload(defaults);
    });
};


djinn.forms.remove_attachment = function(elt, attachment_id) {

  var input = $(elt.parents(".fileupload").find("input[type='file']").eq(0).data("valuefield"));

  pg.remove_value(input, attachment_id, ",");

  $(document).triggerHandler("djinn_forms_fileupload_remove", elt);
};


/**
 * Initialize the relate widget.
 * @param widget Element to initialize.
 */
djinn.forms.initRelateWidget = function(widget) {

  widget.find(".autocomplete").each(function() {
      
      var input = $(this);
      widget.find(".add-list").val("");
      widget.find(".rm-list").val("");
      input.val("");
      
      input.autocomplete({
          source: input.data("search_url"),
            minLength: input.data("search_minlength"),
            select: function(e, ui) {
            input.val(ui.item.label);
            input.data("urn", ui.item.value);
            e.preventDefault();
          }
        });
    });
};


$(document).ready(function() {
        
    $(".relate").each(function() {
        djinn.forms.initRelateWidget($(this));
      });

    $(document).on("click", ".relate .add", function(e) {

        var input = $(e.currentTarget).parents(".relate").find(".autocomplete");
        var widget = $(e.currentTarget).parents(".relate");
        var tpl = widget.find("ul .tpl").eq(0).clone();

        e.preventDefault();
        e.stopPropagation();

        if (!(input.val() && input.data("urn"))) {
          return;
        }

        djinn.forms.addValue(widget.find(".add-list").eq(0),
                             input.data("urn"));

        tpl.attr("class", "");
        tpl.attr("style", "");
        tpl.find("a").eq(0).html(input.val());
        tpl.find("a").eq(1).data("urn", input.data("urn"));

        widget.find("ul").append(tpl);

        input.val("");
        input.data("urn", "");
      });

    $(document).on("click", ".relate .delete", function(e) {

        e.preventDefault();
        
        var widget = $(e.currentTarget).parents(".relate");
        var record = $(e.currentTarget).parents("li");
        var link = $(e.currentTarget);

        djinn.forms.removeValue(widget.find(".add-list").eq(0), 
                                link.data("urn"));
        djinn.forms.addValue(widget.find(".rm-list").eq(0),
                             link.data("urn"));

        record.remove();
      });
  });