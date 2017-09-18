$(document).ready(function() {
    $("#linkList").hide();
    $("#scrapyGif").hide();
    $("#scrapyForm").on("submit", function() {
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
                    tbody_html += "<td>" + result.res_data[i].url_text + "</td>"
                                + "<td><a href=\"" + result.res_data[i].url_link +"\" target=\"_blank\">"
                                +   result.res_data[i].url_link + "</a></td>"
                                + "</tr>";
                }
                $("#url_tbody").html(tbody_html);
                $("#linkList").val("");
                $("#scrapyError").text("Successfull");
                $("#submitBtn").prop("disabled", false);
                $("#scrapyGif").hide();
            },
            error: function (responseRes, textStatus, errorThrown) {
                if(responseRes.status === 500) {
                    $("#scrapyError").html(responseRes.responseJSON.msg);
                }
                else {
                    $("#scrapyError").text("Error during connecting server..");
                }
                $("#submitBtn").prop("disabled", false);
                $("#scrapyGif").hide();
            }
        });
        return false;
    });
});