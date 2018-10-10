
$(function () {
    select_init();
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
            var item = data["item"]
            var html = '<optgroup label="' + data["name"] + '">\n'
            for (var i = 0; i < item.length; i++) {
                html += '<option value="' + item[i].id + '">' + item[i].item_name + '</option>\n'
            }
            html += '</optgroup>'
            $('.user_add_material').append(html)
        }
    })
}