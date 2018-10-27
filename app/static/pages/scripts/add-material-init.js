$(function () {
    select_init();
    $('#material_parent').change(function () {
        select_item();
        //第二次点击parent，child任然有值，修改此处存在问题
        check_material_child('parent_clear');
    });
    $('#material_child').change(function () {
        check_material_child();
        get_child_val();
    });
})

function select_init() {
    //get parameters for url
    var get_param = location.search.replace('?id=', '');
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
    get_child = $('#material_child option:selected').val();
    if (get_child !== null && get_child !== undefined) {
        var new_url = '/manage/user_add_material_details?item_id=' + get_child;
        $('#item_next').attr('href', new_url)
    } else {
        $('#item_next').attr('disabled', 'disabled')
    }

}