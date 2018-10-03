$(function () {

    $(".js-delete-post").click(function () {
        var btn = $(this);
        $("#modal-post").modal("show");
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $("#modal-post .modal-body").html(data.html_form);
            }
        });
    });

    $("#modal-post").on("submit", ".js-post-delete-form", function () {
        var form = $(this);
        var id = form.serializeArray().find(v => v.name === "id").value;
        console.log(id)
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            dataType: 'json',
            success: function (data) {

                    $("#post_" + id).remove();

                    $("#modal-post").modal("hide");
                }

        });
        return false;
    });
    $(".js-update-post").click(function () {
        var btn = $(this);
        $("#modal-post").modal("show");
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $("#modal-post .modal-body").html(data.html_form);
            }
        });
    });


    $("#modal-post").on("submit", ".js-post-update-form", function (event) {
        var form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),

            success: function (data) {
                if (data.form_is_valid) {

                    $("#title_" + data.id).text(data.title);
                    $("#text_" + data.id).html(data.text);
                    $("#modal-post").modal("hide");  // <-- Close the modal
                }
                else {

                    $("#modal-post .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    });
});
