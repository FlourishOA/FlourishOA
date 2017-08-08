$(document).ready(function() {
    if ($('#id_currency').find(":selected").text() != 'OTHER') {
        $("label[for='id_other']").hide();
        $('#id_other').hide();
    }
});

$(document).on('change','#id_currency',function() {
    if ($('#id_currency').find(":selected").text() == 'OTHER') {
        $("label[for='id_other']").show();
        $('#id_other').show();
    }
    else {
        $("label[for='id_other']").hide();
        $('#id_other').hide();
    }
});