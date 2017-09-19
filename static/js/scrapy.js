function getSuccess(result)
{
    tbody_html = "";
    var page_url = "";
    for(var i in result.res_data) {
        tbody_html += "<tr>";
        if(page_url === result.res_data[i].page_url){
            tbody_html += "<td>  </td>";
        }
        else {
            tbody_html += "<td><a href=\"" + result.res_data[i].page_url +"\" target=\"_blank\">"
                        + result.res_data[i].page_url + "</a></td>";
            page_url = result.res_data[i].page_url;
        }
        tbody_html += "<td><a href=\"" + result.res_data[i].link +"\" target=\"_blank\">"
                    +   result.res_data[i].link + "</a></td>"
                    + "<td>" + result.res_data[i].link_type + "</td>"
                    + "</tr>";
    }
    if(result.res_data.length === 0) {
        tbody_html = "<tr><td></td><td>No Data</td><td></td></tr>";
    }
    $("#url_tbody").html(tbody_html);
    $("#scrapyGif").hide();
}

function getError(responseRes, textStatus, errorThrown)
{
    if(responseRes.status === 500 || responseRes.status === 400) {
        $("#scrapyError").html(responseRes.responseJSON.msg);
    }
    else {
        $("#scrapyError").text("Error during connecting server..");
    }
    $("#submitBtn").prop("disabled", false);
    $("#scrapyGif").hide();
}

function linkTypeFilter()
{
    $("#scrapyGif").show();
    $.ajax({
        type: "GET",
        url: "/urlFilter/",
        data: {
            start_url: $("#start_url").val(),
            link_type: $("#link_type").val()
        },
        success: getSuccess,
        error: getError
    });
    return false;
}

$(document).ready(function() {
    $("#scrapyGif").hide();
    $("#scrapyForm").on("submit", function() {
        var start_url = $("#start_url").val().trim();
        var protocol = start_url.split("/")[0];
        if(protocol !== "http:" && protocol !== "https:") {
            $("#scrapyError").text("Please prepend http or https.");
            return false;
        }
        $("#start_url").val(start_url);
        $("#scrapyGif").show();
        $("#submitBtn").prop("disabled", true);
        var formData = new FormData($("#scrapyForm")[0]);
        $.ajax({
            type: "POST",
            url: "/ScrapyView/",
            data: formData,
            processData: false,
            contentType: false,
            success: function(result) {
                linkTypeFilter();
                $("#scrapyError").text("Successfull");
                $("#submitBtn").prop("disabled", false);
            },
            error: getError
        });
        return false;
    });
    // On change filter boxes
    $("#link_type").on("change", function() {
        linkTypeFilter();
    });
});