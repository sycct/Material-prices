$(function () {
    var url_param = get_url_param();
    change_select_item(url_param);
    set_property_value(url_param, pro_id())
});

var get_url_param = function () {
    var url_string = window.location.href;
    var url = new URL(url_string);
    var get_item_id = url.searchParams.get("item_id");
    if (get_item_id === null) {
        return false;
    } else {
        return get_item_id;
    }
};

var pro_id = function () {
    var url_string = window.location.href;
    var url = new URL(url_string);
    var get_item_id = url.searchParams.get("pro_id");
    if (get_item_id === null) {
        return false;
    } else {
        return get_item_id;
    }
};

function change_select_item(param) {
    $.ajax({
        type: 'GET',
        url: '/manage/ajax_get_material_item',
        data: {get_id: param, filter: "item"},
        contentType: "json",
        success: function (data) {
            var html = '';
            for (var i = 0; i < data.length; i++) {
                html += '<option value="' + data[i].id + '">' + data[i].name + '</option>'
            }
            $('#value_to_item_name').append(html)
        }
    })
}

function set_property_value(param, pro_id) {
    $.ajax({
        type: 'GET',
        url: '/manage/ajax_list_pro_name',
        data: {get_id: param, filter: "pro_name"},
        contentType: "json",
        success: function (data) {
            var html = '';
            for (var i = 0; i < data.length; i++) {
                if (data[i].id == pro_id) {
                    html += '<option value="' + data[i].id + '" selected>' + data[i].name + '</option>'
                } else {
                    html += '<option value="' + data[i].id + '">' + data[i].name + '</option>'
                }
            }
            $('#value_to_pro_name').append(html)
        }
    })
}