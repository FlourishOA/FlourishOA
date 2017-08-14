$(document).ready(function() {
    $("#id_search_query").keyup(function() {
        getData($("#id_search_query").val());
    });
});

$(document).on("mouseover", ".ui-menu-item", function() {
    $(this).css("background-color", "#ADD8E6");
});

$(document).on("mouseout", ".ui-menu-item", function() {
    $(this).css("background-color", "white");
})


function getData(value) {
    $.ajax({
        async: false,
        type: 'GET',
        url: '/jname-autocomplete/?q=' + value,
        dataType: "JSON",
        success: function(data) {
            arr = [];
            if (data["results"]) {
                for (var index = 0; index < data["results"].length; index++) {
                    arr.push(data.results[index].text.substring(11) + " (ISSN: " + data.results[index].text.substring(0, 9) + ")");
                }
            }
            complete(arr);
        }
    });
}

function complete(arr) {
    $("#id_search_query").autocomplete({
        appendTo: "#container",
        minLength: 2,
        source: arr,
    });
}