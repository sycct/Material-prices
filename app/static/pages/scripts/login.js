var Login = function () {

    var handleLogin = function () {

        $('.login-form').validate({
            errorElement: 'span', //default input error message container
            errorClass: 'help-block', // default input error message class
            focusInvalid: false, // do not focus the last invalid input
            rules: {
                username: {
                    required: true
                },
                password: {
                    required: true
                },
                remember: {
                    required: false
                }
            },

            messages: {
                username: {
                    required: "Username is required."
                },
                password: {
                    required: "Password is required."
                }
            },

            invalidHandler: function (event, validator) { //display error alert on form submit
                $('.alert-danger', $('.login-form')).show();
            },

            highlight: function (element) { // hightlight error inputs
                $(element)
                    .closest('.form-group').addClass('has-error'); // set error class to the control group
            },

            success: function (label) {
                label.closest('.form-group').removeClass('has-error');
                label.remove();
            },

            errorPlacement: function (error, element) {
                error.insertAfter(element.closest('.input-icon'));
            },

            submitHandler: function (form) {
                form.submit(); // form validation success, call ajax form submit
            }
        });

        $('.login-form input').keypress(function (e) {
            if (e.which == 13) {
                if ($('.login-form').validate().form()) {
                    $('.login-form').submit(); //form validation success, call ajax form submit
                }
                return false;
            }
        });
    }

    var handleForgetPassword = function () {
        $('.forget-form').validate({
            errorElement: 'span', //default input error message container
            errorClass: 'help-block', // default input error message class
            focusInvalid: false, // do not focus the last invalid input
            ignore: "",
            rules: {
                email: {
                    required: true,
                    email: true
                }
            },

            messages: {
                email: {
                    required: "Email is required."
                }
            },

            invalidHandler: function (event, validator) { //display error alert on form submit

            },

            highlight: function (element) { // hightlight error inputs
                $(element)
                    .closest('.form-group').addClass('has-error'); // set error class to the control group
            },

            success: function (label) {
                label.closest('.form-group').removeClass('has-error');
                label.remove();
            },

            errorPlacement: function (error, element) {
                error.insertAfter(element.closest('.input-icon'));
            },

            submitHandler: function (form) {
                form.submit();
            }
        });

        $('.forget-form input').keypress(function (e) {
            if (e.which == 13) {
                if ($('.forget-form').validate().form()) {
                    $('.forget-form').submit();
                }
                return false;
            }
        });

    }

    var handleRegister = function () {
        if (jQuery().select2 && $('#country_list').size() > 0) {
            $("#country_list").select2({
                placeholder: '<i class="fa fa-map-marker"></i>&nbsp;Select a Country',
                width: 'auto',
                escapeMarkup: function (m) {
                    return m;
                }
            });

            $('#country_list').change(function () {
                $('.register-form').validate().element($(this)); //revalidate the chosen dropdown value and show error or success message for the input
                var ID = $(this).val();
                $.ajax({
                    type: "POST",
                    url: '/auth/country',
                    dataType: 'json',
                    data: {country: ID},
                    success: function (data) {
                        $('#select2-city_list-container').empty();
                        //var html = '';
                        var itemList = [];
                        $.each(data, function (Index, CityName) {
                            itemList.push({id: CityName['0'], text: CityName['1']})
                            //html += '<option value=' + CityName['0'] + '>' + CityName['1'] + '</option>'
                            console.log(itemList)
                        });
                        $('#city_list').select2({
                            placeholder: '<i class="fa fa-map-marker"></i>&nbsp;Select a City',
                            width: 'auto',
                            data: itemList
                        });
                         $("#city_list").change();
                        /*$.each(data, function (Index, CityName) {
                            itemList.push({id: CityName['0'], text: CityName['1']})
                            //html += '<option value=' + CityName['0'] + '>' + CityName['1'] + '</option>'
                        });*/
                        //$('#city_list').html(html);
                    }
                });
            });
        }

     if (jQuery().select2 && $('#city_list').size() > 0) {
            $("#city_list").select2({
                placeholder: '<i class="fa fa-map-marker"></i>&nbsp;Select a City',
                width: 'auto',
                escapeMarkup: function (m) {
                    return m;
                },
            });

            $('#city_list').change(function () {
                $('.register-form').validate().element($(this));
            })
        }

    $('.register-form').validate({
        errorElement: 'span', //default input error message container
        errorClass: 'help-block', // default input error message class
        focusInvalid: false, // do not focus the last invalid input
        ignore: "",
        rules: {

            fullname: {
                required: true
            },
            email: {
                required: true,
                email: true
            },
            address: {
                required: true
            },
            city: {
                required: true
            },
            country: {
                required: true
            },

            username: {
                required: true
            },
            password: {
                required: true
            },
            rpassword: {
                equalTo: "#register_password"
            },

            tnc: {
                required: true
            }
        },

        messages: { // custom messages for radio buttons and checkboxes
            tnc: {
                required: "Please accept TNC first."
            }
        },

        invalidHandler: function (event, validator) { //display error alert on form submit

        },

        highlight: function (element) { // hightlight error inputs
            $(element)
                .closest('.form-group').addClass('has-error'); // set error class to the control group
        },

        success: function (label) {
            label.closest('.form-group').removeClass('has-error');
            label.remove();
        },

        errorPlacement: function (error, element) {
            if (element.attr("name") == "tnc") { // insert checkbox errors after the container
                error.insertAfter($('#register_tnc_error'));
            } else if (element.closest('.input-icon').size() === 1) {
                error.insertAfter(element.closest('.input-icon'));
            } else {
                error.insertAfter(element);
            }
        },

        submitHandler: function (form) {
            form.submit();
        }
    });

    $('.register-form input').keypress(function (e) {
        if (e.which == 13) {
            if ($('.register-form').validate().form()) {
                $('.register-form').submit();
            }
            return false;
        }
    });
}

return {
    //main function to initiate the module
    init: function () {

        handleLogin();
        handleForgetPassword();
        handleRegister();

    }

};

}
();

jQuery(document).ready(function () {
    Login.init();
});