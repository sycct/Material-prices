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
            if (data == 1) {
                Alert_common('.profile-content', 'warning', '更新失败！', 'warning');
            } else {
                var html = ''
                brand = 'brand'
                var item = data['data']
                for (i = 0; i < item.length; i++) {
                    html += '<tr>\n' +
                        '                                            <td> ' + i + '</td>\n' +
                        '                                            <td> ' + item[i]["brand_name"] + ' </td>\n' +
                        '                                            <td>' + item[i]["brand_since"] + '</td>\n' +
                        '                                            <td>\n' +
                        '                                                <a class="edit" href="/manage/admin_edit_brand/' + item[i]["id"] + '?select=' + get_item_val + '">Edit </a>\n' +
                        '                                            </td>\n' +
                        '                                            <td>\n' +
                        '                                                <a class="delete" onclick="show_delete_modal(' + "brand" + ',' + item[i]["id"] + ')">Delete </a>\n' +
                        '                                            </td>\n' +
                        '                                        </tr>'
                }
                $('#brand_table').empty();
                $('#brand_table').append(html);
            }
        }
    });
}