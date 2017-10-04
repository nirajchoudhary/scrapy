function getSuccess(result)
{
    var pagination = "";
    if(result.url_page.hasOtherPages) {
        if(result.url_page.hasPreviousPage) {
            pagination += "<li class=\"page-item\" title=\"First page\" onclick=\"return linkTypeFilter(1);\"><a class=\"page-link\" href=\"#\">&laquo;</a></li>";
            pagination += "<li class=\"page-item\" title=\"Previous page\" onclick=\"return linkTypeFilter(" + result.url_page.previousPageNo + ");\"><a class=\"page-link\" href=\"#\">&lsaquo;</a></li>";
        }
        else {
            pagination += "<li class=\"page-item disabled\" title=\"First page\"><a class=\"page-link\" href=\"#\">&laquo;</a></li>";
            pagination += "<li class=\"page-item disabled\" title=\"Previous page\"><a class=\"page-link\" href=\"#\">&lsaquo;</a></li>";
        }
        totalPage = result.url_page.totalPage;
        $("#totalPage").html("&nbsp; Total Pages in Pagination: " + totalPage);
        for(var i in result.url_page.pageRange) {
            var pageLinkNo = result.url_page.pageRange[i];
            if(result.url_page.currentPage === pageLinkNo) {
                pagination += "<li class=\"page-item active\"><a class=\"page-link\" href=\"#\">" + pageLinkNo  + "</a></li>";
            }
            else {
                pagination += "<li class=\"page-item\" onclick=\"return linkTypeFilter(" + pageLinkNo + ");\"><a class=\"page-link\" href=\"#\">" + pageLinkNo + "</a></li>";
            }
        }
        if(result.url_page.hasNextPage) {
            pagination += "<li class=\"page-item\" title=\"Next page\" onclick=\"return linkTypeFilter(" + result.url_page.nextPageNo + ");\"><a class=\"page-link\" href=\"#\">&rsaquo;</a></li>";
            pagination += "<li class=\"page-item\" title=\"Last page\" onclick=\"return linkTypeFilter(" + totalPage + ");\"><a class=\"page-link\" href=\"#\">&raquo;</a></li>";
        }
        else {
            pagination += "<li class=\"page-item disabled\" title=\"Next page\"><a class=\"page-link\" href=\"#\">&rsaquo;</a></li>";
            pagination += "<li class=\"page-item disabled\" title=\"Last page\"><a class=\"page-link\" href=\"#\">&raquo;</a></li>";
        }
    }
    else {
        $("#totalPage").html("");
    }
    tbody_html = "";
    var page_url = "";
    for(var i in result.res_data) {
        tbody_html += "<tr>";
        if(result.res_data[i].link_count > 0) {
            if(page_url === result.res_data[i].page_url){
                tbody_html += "<td>  </td>";
            }
            else {
                tbody_html += "<td><a class=\"urlBreak\" href=\"" + result.res_data[i].page_url +"\" target=\"_blank\">"
                            + result.res_data[i].page_url + "</a><br>(Total Links: "
                            + result.res_data[i].link_count + ")</td>";
                page_url = result.res_data[i].page_url;
            }
            tbody_html += "<td class=\"link_td\"><a href=\"" + result.res_data[i].link +"\" target=\"_blank\" class=\"urlBreak\">"
                        +   result.res_data[i].link + "</a></td>"
                        + "<td class=\"category_td\">" + result.res_data[i].url_category + "</td>"
                        + "<td class=\"link_type_td\">" + result.res_data[i].link_type + "</td>"
                        + "</tr>";
        }
        else {
            tbody_html += "<td><a class=\"urlBreak\" href=\"" + result.res_data[i].page_url +"\" target=\"_blank\">"
                        + result.res_data[i].page_url + "</a><br>(Total Link: "
                        + result.res_data[i].link_count + ")</td>"
                        + "<td>No link on this page</td>"
                        + "<td>unknown</td><td>unknown</td>"
                        + "</tr>";
        }
    }
    if(result.res_data.length === 0) {
        tbody_html = "<tr><td></td><td>No Data</td><td></td><td></td></tr>";
    }
    if(result.row_count < 2) {
        $("#row_count").text(result.row_count + " record");
    }
    else {
        $("#row_count").text(result.row_count + " records");
    }

    if(result.page_count < 2) {
        $("#page_count").html("&nbsp;(Total Page: " + result.page_count + ")");
    }
    else {
        $("#page_count").html("&nbsp;(Total Pages: " + result.page_count + ")");
    }

    $("#url_tbody").html(tbody_html);
    $("#urlPagination").html(pagination);
    if(result.is_finished) {
        $("#job_id").val("");
        $("#scrapyError").text(result.msg);
        $("#scrapyGif").hide();
    }
    else {
        setTimeout(function() {
            linkTypeFilter(1);
        }, 5000);
    }
}

function getError(responseRes, textStatus, errorThrown)
{
    if(responseRes.status === 500 || responseRes.status === 400 || responseRes.status === 404) {
        $("#scrapyError").html(responseRes.responseJSON.msg);
    }
    else if(responseRes.status === 401) {
        window.location.replace("/Login/");
    }
    else {
        $("#scrapyError").text("Error during connecting server..");
    }
    $("#job_id").val("");
    $("#submitBtn").prop("disabled", false);
    $("#newFetchBtn").prop("disabled", false);
    $("#scrapyGif").hide();
}

function linkTypeFilter(page_no)
{
    $("#scrapyGif").show();
    $.ajax({
        type: "GET",
        url: "/urlFilter/",
        data: {
            job_id: $("#job_id").val(),
            start_url: $("#start_url").val(),
            depth: $("#depth").val(),
            link_type: $("#link_type").val(),
            page_URL: $("#page_URL").val(),
            category: $("#category").val(),
            link_input: $("#link_input").val(),
            page_no: page_no,
        },
        success: getSuccess,
        error: getError
    });
    return false;
}

$(document).ready(function() {
    $("#scrapyGif").hide();
    // $('[data-toggle="tooltip"]').tooltip();

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
            timeout: 3000000,
            processData: false,
            contentType: false,
            success: function(result) {
                $("#scrapyError").text(result.msg);
                $("#job_id").val(result.job_id);
                linkTypeFilter(1);
                $("#submitBtn").prop("disabled", false);
                $("#newFetchBtn").prop("disabled", false);
            },
            error: getError
        });
        return false;
    });
    // On change filter boxes
    $("#link_type").on("change", function() {
        linkTypeFilter(1);
    });
    $("#category").on("change", function() {
        linkTypeFilter(1);
    });
    $("#page_URL").on("autocompleteselect", function (e, ui) {
        $("#page_URL").val(ui.item.value);
        linkTypeFilter(1);
    });
    $("#searchPageURLBtn").on("click", function(){
        linkTypeFilter(1);
        return false;
    });
    $("#pageURLForm").on("submit", function() {
        linkTypeFilter(1);
        return false;
    });
    $("#link_input").on("autocompleteselect", function (e, ui) {
        $("#link_input").val(ui.item.value);
        linkTypeFilter(1);
    });
    $("#searchLinkBtn").on("click", function(){
        linkTypeFilter(1);
        return false;
    });
    $("#linkForm").on("submit", function() {
        linkTypeFilter(1);
        return false;
    });
    $("#page_URL").on('input keyup', function() {
        var start_url = $("#start_url").val();
        var depth = $("#depth").val();
        $("#page_URL").autocomplete({
            source: "/getPageURL/?start_url=" + start_url + "&depth=" + depth,
            minLength: 2,
            autoFocus: true,
        });
    });
    $("#link_input").on('input keyup', function() {
        var start_url = $("#start_url").val();
        var depth = $("#depth").val();
        $("#link_input").autocomplete({
            source: "/getLink/?start_url=" + start_url + "&depth=" + depth,
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
            timeout: 3000000,
            data: {
                start_url: $("#start_url").val(),
                depth: $("#depth").val()
            },
            success: function(result) {
                $("#scrapyError").text(result.msg);
                $("#job_id").val(result.job_id);
                linkTypeFilter(1);
                $("#submitBtn").prop("disabled", false);
                $("#newFetchBtn").prop("disabled", false);
            },
            error: getError
        });
        return false;
    });
});