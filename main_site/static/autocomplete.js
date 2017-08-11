$(document).ready(function() {
    $("#id_search_query").keyup(function() {
        getData($("#id_search_query").val());
    });
});



function getData(value) {
    $.ajax({
        async: false,
        type: 'GET',
        url: '/jname-autocomplete/?q=' + value,
        dataType: "JSON",
        success: function(data) {
            console.log(data);
            arr = [];
            if (data["results"]) {
                for (var index = 0; index < data["results"].length; index++) {
                    arr.push(data.results[index].text.substring(11) + " (ISSN:" + data.results[index].text.substring(0, 10) + ")");
                }
            }
            complete(arr);
        }
    });
}

function complete(arr) {
    var autocomplete;
    console.log(arr);
    $("#id_search_query").autocomplete({
        minLength: 2,
        source: arr,
    });
    console.log($("#id_search_query").autocomplete("widget"));
}