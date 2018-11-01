$(function () {
    change_select_item();
})

function change_select_item() {
    get_item_str = location.search;
    get_item_length = get_item_str.length;
    get_item_index = get_item_str.indexOf('item_id=')
    get_item_id = get_item_str.substr(get_item_index + 'item_id='.length, get_item_length)
    if (get_item_id == null) {
        return false;
    } else {
        $.ajax({
            type: 'GET',
            url: '/manage/ajax_get_material_item',
            data: {get_id: get_item_id},
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
}