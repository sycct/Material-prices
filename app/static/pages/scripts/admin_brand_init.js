$(function () {
    init_brand();
})

function init_brand() {
    var get_item_str = location.search;
    var get_item_length = get_item_str.length;
    var get_item_index = get_item_str.indexOf('item_id=')
    var get_item_id = get_item_str.substr(get_item_index + 'item_id='.length, get_item_length)
    console.log(get_item_id)
    if (get_item_id == "") {
        return false;
    }
    $.ajax({
        type: 'GET',
        url: '/manage/ajax_get_item',
        data: {ajax_item_id: get_item_id},
        contentType: "json",
        success: function (data) {
            var html = '';
            $('#Brand_to_Item').empty();
            for (var i = 0; i < data.length; i++) {
                if (data[i].id == get_item_id) {
                    html += '<option value="' + data[i].id + '" selected>' + data[i].i_name + '</option>'
                } else {
                    html += '<option value="' + data[i].id + '">' + data[i].i_name + '</option>'
                }
            }
            $('#Brand_to_Item').append(html)
        }
    })
}