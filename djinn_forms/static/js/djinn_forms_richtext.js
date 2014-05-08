/**
 * Djinn form richtext config
 */

if (djinn === undefined) {
  var djinn = {};
}

if (djinn.forms === undefined) {
  djinn.forms = {};
}

djinn.forms.richtext = {
  BUTTONS: "bold,italic,underline,strikethrough,|,sub,sup,|,justifyleft,justifycenter,justifyright,justifyfull,|,indent,outdent,|,bullist,numlist,|,cleanup,code,|,table,|,link,unlink,anchor",
  TINYMCE_PLUGINS: "lists,pagebreak,table,paste,directionality,visualchars,nonbreaking",
};

/**
 * Add button to tiny for links.
 * @param ed editor instance
 */
djinn.forms.richtext.setup_link_plugin = function(ed) {

  ed.addButton('link', {
    title : 'Link',
    image : '/static/img/link.png',
    onclick : function() {

      document.cur_wysiwyg = ed;

      ed.windowManager.bookmark = ed.selection.getBookmark();

      elt = ed.selection.getNode();

      var parents = ed.dom.getParents(elt);
      var currlink = "";

      for (var i = 0; i < parents.length; i++) {

        if (parents[i].nodeName == "A") {
          currlink = ed.dom.getAttrib(parents[i], 'href');
          break;
        }
      }

      var remote_url = '/contentlinks/?callbackOnSelect=djinn.forms.richtext.insert_in_wysiwyg&currlink=' + encodeURIComponent(currlink);

      $.get(remote_url,
            function(data) {
              djinn.contenttypes.show_modal(data);
            }
           );
    }
  });
};

/**
 * Add button to tiny for images. This method must also pass any
 * attachments that have not yet been added to the content.
 * @param ed editor instance
 */
djinn.forms.richtext.setup_img_plugin = function(ed, ctype, cid, img_type) {

  var widget = $("#" + ed.editorId).parents(".richtext").find("textarea");

  ed.addButton('image', {
    title : 'Afbeeldingen',
    image : '/static/img/img.png',
    onclick : function() {
      document.cur_wysiwyg = ed;

      var image_ids = $(":hidden[name=images]").first().val() || "";

      $.get("/contentimages/" + ctype + "/" + cid,
            {"image_ids": image_ids, "img_type": img_type},
            function(data) {
              djinn.contenttypes.show_modal(data, [widget]);
            }
           );
    }});
};


djinn.forms.richtext.TINYMCE_CONFIG = {

  script_url : '/static/jquery.tinymce/jscripts/tiny_mce/tiny_mce.js',
  content_css : '/static/css/tinymce_custom.css',

  // General options
  theme : "advanced",
  language: "nl",
  plugins : djinn.forms.richtext.TINYMCE_PLUGINS,

  // Theme options
  theme_advanced_buttons1 : djinn.forms.richtext.BUTTONS,
  theme_advanced_buttons2 : "",
  theme_advanced_buttons3 : "",
  theme_advanced_toolbar_location : "top",
  theme_advanced_toolbar_align : "left",
  theme_advanced_resizing : true,
  relative_urls : false,
  cleanup_on_startup : true,
  cleanup : true,
};


djinn.forms.richtext.TINYMCE_MAXCHARS_CONFIG = {

  theme_advanced_path : false,
  theme_advanced_statusbar_location : "bottom"
};


djinn.forms.richtext.setup_maxchars = function(ed) {

  ed.onKeyUp.add(function(ed, e) {

    var chars = tinyMCE.activeEditor.getBody().textContent.length;
    
    // textcontent skips newlines, so let's find them
    var nls = tinyMCE.activeEditor.getBody().innerHTML.split("<br>").length - 1;
    
    chars = chars + nls;
    
    var text = chars + " tekens";
    tinymce.DOM.setHTML(tinymce.DOM.get(tinyMCE.activeEditor.id + '_path_row'), text);
  });
};

/**
 *  Callback function (see above) specifically intended for tinymce editors.
 *  The selected item will be inserted as a link in the
 *  tinymce wysiwyg with title as the clickable text
 *
 * @param url
 * @param content_type
 * @param object_id
 * @param title
 * @param extra_args Associative array of options. 'target' is used, if given,
 * to insert link and add target for href.
 */
djinn.forms.richtext.insert_in_wysiwyg = function(url, content_type,
                                                  object_id, title,
                                                  extra_args) {

  var ed = document.cur_wysiwyg;

  ed.selection.moveToBookmark(ed.windowManager.bookmark);

  selectedtext = ed.selection.getContent({format : 'text'}) || title;

  html = '<a href="' + url + '" class="' + content_type + '"';

  if (extra_args && extra_args.target) {
    html += ' target="' + extra_args.target + '">' + selectedtext + '</a>';
  } else {
    html += '>' + selectedtext + '</a>';
  }

  ed.execCommand("mceInsertContent", false, html);
};


/**
 * Insert image into current wysiwyg.
 * @param position One of left, right or center
 * @param img_url URL of full image
 * @param url URL of image.
 */
djinn.forms.richtext.insert_image_wysiwyg = function(position, img_url, url) {

  var ed = document.cur_wysiwyg;

  html = '<a data-target="#MyModal" data-toggle="modal" class="modal-image" href="' + img_url + '"><img style="float: ' + position + ';margin: 5px 20px 5px 0px" src="' + url + '"/></a>';

  if (position == "center") {
    html = '<div style="text-align: center"><a data-target="#MyModal" data-toggle="modal" class="modal-image" href="' + img_url + '"><img src="' + url + '"/></a></div>';
  }

  ed.execCommand("mceInsertContent", false, html);
};


/**
 * Extend jQuery with richtext call.
 */
(function($) {

  /**
   * RichText initializer, with ctype and cid of context, if
   * available. Based on that, either images can be added or not.
   * @param ctype Content type
   * @param cid Content id. May be undefined for new content
   * @param options dict of options
   */
  $.fn.richtext = function(ctype, cid, img_type, options) {

    var config = $.extend({}, djinn.forms.richtext.TINYMCE_CONFIG);

    var settings = $.extend({
      // These are the defaults.
      maxchars: -1,
      hresize: false,
      plugins: djinn.forms.richtext.TINYMCE_PLUGINS,
      config: config
    }, options);

    if (settings.maxchars > -1) {
      settings.plugins += ",maxlength";

      $.extend(settings.config, djinn.forms.richtext.TINYMCE_MAXCHARS_CONFIG);
      $.extend(settings.config, {maxlength_id_summary: settings.maxchars});
    }

    if (settings.hresize) {
      $.extend(settings.config, {theme_advanced_resize_horizontal: 'true'});
    }

    if (ctype && cid) {
      settings.config.theme_advanced_buttons1 += ",image";
    }

    // Determine setup functions
    settings.config.setup = function(ed) {

      djinn.forms.richtext.setup_link_plugin(ed);

      if (settings.maxchars > -1) {
        djinn.forms.richtext.setup_maxchars(ed);
      }

      if (ctype && cid) {
        djinn.forms.richtext.setup_img_plugin(ed, ctype, cid, img_type);
      }      
    };

    return this.tinymce(settings.config);
  };
}(jQuery));


$(document).ready(function() {

  $(".richtext").each(function() {
    var input = $(this).find("textarea");

    var options = {};

    if (input.data("maxchars")) {
      options.maxchars = input.data("maxchars");
    }

    input.richtext(input.data("ctype"), input.data("cid"),
                   input.data("img_type"), options);
  });

  $(document).on("hide", ".modal", function(e) {

    $(e.currentTarget).removeData('modal');
  });

  $(document).on("modal_action_show", "#contentimages", function(e, widget) {

    var modal = $(e.target);

    modal.find(".controls a").click(function(e) {

      e.preventDefault();
      
      var link = $(e.currentTarget);
      
      djinn.forms.richtext.insert_image_wysiwyg(link.data("pos"),
                                                link.attr("href"),
                                                link.data("img"));

      modal.modal('hide');

      document.cur_wysiwyg.focus();
    });
  });
});