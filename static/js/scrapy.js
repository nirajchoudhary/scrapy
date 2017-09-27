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
            tbody_html += "<td ><a class=\"urlBreak\" href=\"" + result.res_data[i].page_url +"\" target=\"_blank\">"
                        + result.res_data[i].page_url + "</a></td>";
            page_url = result.res_data[i].page_url;
        }
        tbody_html += "<td class=\"link_td\"><a href=\"" + result.res_data[i].link +"\" target=\"_blank\" class=\"urlBreak\">"
                    +   result.res_data[i].link + "</a></td>"
                    + "<td class=\"category_td\">" + result.res_data[i].url_category + "</td>"
                    + "<td class=\"link_type_td\">" + result.res_data[i].link_type + "</td>"
                    + "</tr>";
    }
    if(result.res_data.length === 0) {
        tbody_html = "<tr><td></td><td>No Data</td><td></td><td></td></tr>";
    }
    if(result.row_count === 0) {
        $("#row_count").text(result.row_count + " record");
    }
    else {
        $("#row_count").text(result.row_count + " records");
    }
    $("#url_tbody").html(tbody_html);
    $("#scrapyGif").hide();
}

function getError(responseRes, textStatus, errorThrown)
{
    if(responseRes.status === 500 || responseRes.status === 400 || responseRes.status === 404) {
        $("#scrapyError").html(responseRes.responseJSON.msg);
    }
    else {
        $("#scrapyError").text("Error during connecting server..");
    }
    $("#submitBtn").prop("disabled", false);
    $("#newFetchBtn").prop("disabled", false);
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
            depth: $("#depth").val(),
            link_type: $("#link_type").val(),
            page_URL: $("#page_URL").val(),
            category: $("#category").val(),
            link_input: $("#link_input").val()
        },
        success: getSuccess,
        error: getError
    });
    return false;
}

$(document).ready(function() {
    $("#scrapyGif").hide();
    $('[data-toggle="tooltip"]').tooltip();
    $("#scrapyForm").on("submit", function() {
        var start_url = $("#start_url").val().trim();
        var protocol = start_url.split("/")[0];
        if(protocol !== "http:" && protocol !== "https:") {
            $("#scrapyError").text("Please prepend URL with http or https.");
            return false;
            $("#scrapyGif").hide();
        }
        $("#start_url").val(start_url);
        $("#scrapyGif").show();
        $("#submitBtn").prop("disabled", true);
        $("#newFetchBtn").prop("disabled", true);
        var formData = new FormData($("#scrapyForm")[0]);
        $.ajax({
            type: "POST",
            url: "/ScrapyView/",
            data: formData,
            processData: false,
            contentType: false,
            success: function(result) {
                $("#scrapyError").text(result.msg);
                linkTypeFilter();
                $("#submitBtn").prop("disabled", false);
                $("#newFetchBtn").prop("disabled", false);
            },
            error: getError
        });
        return false;
    });
    // On change filter boxes
    $("#link_type").on("change", function() {
        linkTypeFilter();
    });
    $("#category").on("change", function() {
        linkTypeFilter();
    });
    $("#page_URL").on("autocompleteselect", function (e, ui) {
        $("#page_URL").val(ui.item.value);
        linkTypeFilter();
    });
    $("#searchPageURLBtn").on("click", function(){
        linkTypeFilter();
        return false;
    });
    $("#pageURLForm").on("submit", function() {
        linkTypeFilter();
        return false;
    });
    $("#link_input").on("autocompleteselect", function (e, ui) {
        $("#link_input").val(ui.item.value);
        linkTypeFilter();
    });
    $("#searchLinkBtn").on("click", function(){
        linkTypeFilter();
        return false;
    });
    $("#linkForm").on("submit", function() {
        linkTypeFilter();
        return false;
    });
    $("#page_URL").on('input keyup', function() {
        $("#page_URL").autocomplete({
            source: "/getPageURL/?start_url=" + $("#start_url").val(),
            minLength: 2,
            autoFocus: true,
        });
    });
    $("#link_input").on('input keyup', function() {
        $("#link_input").autocomplete({
            source: "/getLink/?start_url=" + $("#start_url").val(),
            minLength: 2,
            autoFocus: true,
        });
    });
    $("#newFetchBtn").on("click", function(){
        $("#scrapyGif").show();
        var start_url = $("#start_url").val().trim();
        var protocol = start_url.split("/")[0];
        if(protocol !== "http:" && protocol !== "https:") {
            $("#scrapyError").text("Please prepend URL with http or https.");
            $("#scrapyGif").hide();
            return false;
        }
        $("#start_url").val(start_url);
        $("#scrapyGif").show();
        $("#submitBtn").prop("disabled", true);
        $("#newFetchBtn").prop("disabled", true);
        $.ajax({
            type: "GET",
            url: "/freshCrawl/",
            data: {
                start_url: $("#start_url").val(),
                depth: $("#depth").val()
            },
            success: function(result) {
                $("#scrapyError").text(result.msg);
                linkTypeFilter();
                $("#submitBtn").prop("disabled", false);
                $("#newFetchBtn").prop("disabled", false);
            },
            error: getError
        });
        return false;
    });
});