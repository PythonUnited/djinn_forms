/**
 * DateTimeDirect widget JS
 */

$(document).ready(function() {
    $.fn.changeradiofunction = function(ctrls){
        $(ctrls).find("input.date").attr("disabled", false);
        $(ctrls).find("input.time").attr("disabled", false);
    }
//    $.fn.changeradiofunction = function(){
//        $("#id_publish_from_date").attr("disabled", false);
//        $("#id_publish_from_time").attr("disabled", false);
//    }

    $('.control-group.datetime').each(function(){
        var ctrls = $(this);
        if ($(ctrls).find("input.date").val() || $(ctrls).find("input.time").val()) {
            $(".notdirectradio").attr("checked", "checked");
            $.fn.changeradiofunction(ctrls);
        }
    });
//    if ($("#id_publish_from_date").val() || $("#id_publish_from_time").val()) {
//        $("#notdirect").attr("checked", "checked");
//        $.fn.changeradiofunction();
//    }

    $('.notdirectradio').each( function(){
        if ($(this).is(':checked')){
            var ctrls = $(this).closest('.controls');
            $.fn.changeradiofunction(ctrls);
        }
    });
//    if($('#notdirect').is(':checked')) {
//        $.fn.changeradiofunction()
//    }

    $('.directradio').change( function () {
        var ctrls = $(this).closest('.controls');

        $(ctrls).find("input.date").attr("disabled", true);
        $(ctrls).find("input.date").attr("value", "");
        $(ctrls).find("input.time").attr("disabled", true);
        $(ctrls).find("input.time").attr("value", "");
//     $('#direct').change( function () {
//        $("#id_publish_from_date").attr("disabled", true);
//        $("#id_publish_from_date").attr("value", "");
//        $("#id_publish_from_time").attr("disabled", true);
//        $("#id_publish_from_time").attr("value", "");
    });

    $('.notdirectradio').change( function () {
        var ctrls = $(this).closest('.controls');
        $(ctrls).find("input.date").attr("disabled", false);
        $(ctrls).find("input.time").attr("disabled", false);
//    $('#notdirect').change( function () {
//        $("#id_publish_from_date").attr("disabled", false);
//        $("#id_publish_from_time").attr("disabled", false);
    });

});
