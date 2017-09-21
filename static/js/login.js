$(document).ready(function() {
    $("#loginGif").hide();
    $("#loginForm").on("submit", function() {
        $("#loginGif").show();
        $("#loginBtn").prop("disabled", true);
        var formData = new FormData($("#loginForm")[0]);
        $.ajax({
            type: "POST",
            url: "/loginView/",
            data: formData,
            processData: false,
            contentType: false,
            success: function(result) {
                $("#loginError").removeClass("text-danger");
                $("#loginError").addClass("text-success");
                $("#loginError").text("Loggedin successfully.");
                window.location.replace(result.redirectTo);
            },
            error: function (responseRes, textStatus, errorThrown) {
                if(responseRes.status === 400) {
                    $("#password").val("");
                    $("#loginError").html(responseRes.responseJSON.msg);
                }
                else {
                    $("#password").val("");
                    $("#loginError").text("Error during connecting server..");
                }
                $("#loginBtn").prop("disabled", false);
                $("#loginGif").hide();
            }
        });
        return false;
    });
});