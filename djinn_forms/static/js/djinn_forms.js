/**
 * Djinn events JS lib
 */

if (djinn == undefined) {
    var djinn = {};
}


djinn.forms = {};


djinn.forms.set_link = function(url, content_type, obj_id, title, extra_args) {

  var val = url + "::" + content_type + "::" + obj_id;
  val += "::" + (extra_args['target'] || "");

  $("#id_" + extra_args['tgt']).val(val);
  $("#" + extra_args['tgt'] + "_link").html(title || url);

  $("#MyModal").modal("hide");
};
