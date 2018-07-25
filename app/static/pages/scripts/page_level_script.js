$(function () {
    $('#user_profile').click(function (event) {
        event.preventDefault();  //prevent the actual form post
        user_profile();
    });

    $('#change_password').click(function (event) {
        event.preventDefault();
        change_password();
    });

    $('#upload_file').click(function (event) {
        event.preventDefault();
        upload_file();
    });

    // Inject our CSRF token into our AJAX request.
    var csrftoken = $('meta[name=csrf-token]').attr('content')

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    })
})

function user_profile() {
    $.ajax({
        type: $('#tab_1_1 form').attr("method"),
        url: $('#tab_1_1 form').attr("action"),
        data: $('#tab_1_1 form').serialize(),
        contentType: "application/x-www-form-urlencoded",
        success: function (data) {

        }
    })
}

function change_password() {
    $.ajax({
        type: $('#tab_1_3 form').attr("method"),
        url: $('#tab_1_3 form').attr("action"),
        data: $('#tab_1_3 form').serialize(),
        contentType: "application/x-www-form-urlencoded",
        success: function (data) {

        }
    })
}

function upload_file() {
    var formData = new FormData();
    formData.append("file", $('#ingredient_file')[0].files[0])
    // add assoc key values, this will be posts values
    $.ajax({
        type: $('#tab_1_2 form').attr("method"),
        url: $('#tab_1_2 form').attr("action"),
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
            console.log(data);
        }
    })
}
