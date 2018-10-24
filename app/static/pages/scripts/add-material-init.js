$(function () {
    select_init();
    check_material_child()
    $('#material_parent').change(function () {
        select_item();
        check_material_child();
    })
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
            var html = ''
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

function check_material_child() {
    var id = $('#material_child option:selected').val();
    alert(id);
    if (id != null && id != undefined) {
        $('#item_next').removeAttr('disabled')
    } else {
        $('#item_next').attr('disabled', 'disabled')
    }
}