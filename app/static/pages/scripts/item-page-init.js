$(function () {
    item_page_init();
    $('#Item_to_Catalog').change(function () {
        item_page_init();
    })
});

function item_page_init() {
    var get_item_val = $('#Item_to_Catalog').val();
    $.ajax({
        type: 'post',
        url: '/manage/admin_get_item',
        data: {item_val: get_item_val},
        contentType: "application/x-www-form-urlencoded",
        success: function (data) {
            if (data == 1) {
                Alert_common('.profile-content', 'warning', '更新失败！', 'warning');
            } else {
                var html = ''
                item_flag = 'item'
                var item = data['data']
                for (var i = 0; i < item.length; i++) {
                    html += '<tr>\n' +
                        '                                            <td> ' + i + '</td>\n' +
                        '                                            <td> ' + item[i]["item_name"] + ' </td>\n' +
                        '                                            <td>\n' +
                        '                                                <a class="edit" href="/manage/admin_edit_item/' + item[i]["id"] + '?select=' + get_item_val + '">Edit </a>\n' +
                        '                                            </td>\n' +
                        '                                            <td>\n' +
                        '                                                <a class="delete" onclick="show_delete_modal(' + "item_flag" + ',' + item[i]["id"] + ')">Delete </a>\n' +
                        '                                            </td>\n' +
                        '                                            <td>\n' +
                        '                                                <a class="add_pro_name" href="/manage/material_property_name?id=' + item[i]["id"] + '">增加属性 </a>\n' +
                        '                                            </td>\n' +
                        '                                            <td>\n' +
                        '                                                <a class="add_brand" href="/manage/admin_add_brand?item_id=' + item[i]["id"] + '">增加品牌 </a>\n' +
                        '                                            </td>\n' +
                        '                                        </tr>'
                }
                $('#catalog_table').empty();
                $('#catalog_table').append(html);
            }
        }
    });
}
