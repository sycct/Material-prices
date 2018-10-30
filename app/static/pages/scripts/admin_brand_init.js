$(function () {
    init_brand();
})

function init_brand() {
    var get_brand_val = location.search.replace("?item_id=", "")
    if (get_brand_val == "") {
        return false;
    }
    $.ajax({
        type: 'GET',
        url: '/manage/ajax_get_item',
        data: {ajax_item_id: get_brand_val},
        contentType: "json",
        success: function (data) {
            var html = '';
            $('#Brand_to_Item').empty();
            for (var i = 0; i < data.length; i++) {
                if (data[i].id == get_brand_val) {
                    html += '<option value="' + data[i].id + '" selected>' + data[i].i_name + '</option>'
                } else {
                    html += '<option value="' + data[i].id + '">' + data[i].i_name + '</option>'
                }
            }
            $('#Brand_to_Item').append(html)
        }
    })
}