/**
 * Djinn events JS lib
 */

if (djinn == undefined) {
    var djinn = {};
}


djinn.forms = {};


djinn.forms.set_link = function(url, content_type, object_id, title, extra_args) {
  var val = url + "::" + content_type + "::" + object_id;

  $("#id_" + extra_args['target']).val(val);
  $("#" + extra_args['target'] + "_link").html(title || url);  
};
