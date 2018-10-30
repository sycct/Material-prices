$(function () {
    init_material_property_name();
})

function init_material_property_name() {
    var get_param = location.search.replace("?id=", "")
    if (get_param === null) {
        return false;
    }
    $.ajax({
        type: 'GET',
        data: {ajax_item_id: get_param},
        url: '/manage/ajax_get_item',
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function (data) {
            var html = ''
            for (var i = 0; i < data.length; i++) {
                if (data[i].id == get_param) {
                    html += '<option value="' + data[i].id + '" selected>' + data[i].i_name + '</option>'
                } else {
                    html += '<option value="' + data[i].id + '">' + data[i].i_name + '</option>'
                }
            }
            $('#item_to_pro_name').append(html);
        }
    });


}