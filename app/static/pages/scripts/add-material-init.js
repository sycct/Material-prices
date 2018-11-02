$(function () {
    select_init();
    $('#material_parent').change(function () {
        select_item();
        check_material_child('parent_clear');
    });
    $('#material_child').change(function () {
        check_material_child();
        get_child_val();
    });
    change_link();
});

function select_init() {
    //get parameters for url
    var get_param = location.search.replace('?classification_id=', '');
    if (get_param == null) {
        return false;
    }
    $.ajax({
        type: 'GET',
        url: '/manage/ajax_get_material',
        data: {get_id: get_param},
        contentType: "json",
        success: function (data) {
            var html = '';
            for (var i = 0; i < data.length; i++) {
                html += '<option value="' + data[i].id + '">' + data[i].name + '</option>'
            }
            $('#material_parent').append(html)
        }
    })
}

function select_item() {
    var id = $('#material_parent option:selected').val();
    $.ajax({
        type: 'GET',
        url: '/manage/ajax_get_material_item',
        data: {get_id: id},
        contentType: "json",
        success: function (data) {
            var html = '';
            $('#material_child').empty();
            for (var i = 0; i < data.length; i++) {
                html += '<option value="' + data[i].id + '">' + data[i].name + '</option>'
            }
            $('#material_child').append(html)
        }
    })
}

function check_material_child(elem) {
    var id;
    id = $('#material_child option:selected').val();
    if (elem === "parent_clear") {
        // clear data.
        id = null;
    }
    if (id != null && id !== undefined) {
        $('#item_next').removeAttr('disabled')
    } else {
        $('#item_next').attr('disabled', 'disabled')
    }
}

function get_child_val() {
    var get_child = $('#material_child option:selected').val();
    if (get_child !== null && get_child !== undefined) {
        var get_classification_id = location.search;
        var new_url = '/manage/user_add_material_details' + get_classification_id + '&item_id=' + get_child;
        $('#item_next').attr('href', new_url)
    } else {
        $('#item_next').attr('disabled', 'disabled')
    }
}

function change_link() {
    var get_uri = location.search;
    var get_a_length = $('div[id^=add_attr_]').length;
    if (get_uri === null) {
        return false;
    } else {
        for (var i = 1; i < get_a_length + 1; i++) {
            var url_str = '#add_attr_' + i + ' a';
            var get_a_href = $(url_str).attr('href');
            $(url_str).attr('href', get_a_href + '&' + get_uri.replace('?', ''))
        }
    }
}