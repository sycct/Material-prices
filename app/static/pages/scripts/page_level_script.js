$(function () {
    $('#user_profile').click(function (event) {
        event.preventDefault();  //prevent the actual form post
        user_profile();
        console.log($('#tab_1_1 form').serialize())
    });

    // Inject our CSRF token into our AJAX request.
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", $('#csrf_token').val())
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