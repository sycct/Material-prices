$(function () {
    catalog_page_init();
    $('#Catalog_to_Classification').change(function () {
        catalog_page_init();
    })
});

function catalog_page_init() {
    var get_catalog_val = $('#Catalog_to_Classification').val();
    $.ajax({
        type: 'post',
        url: '/manage/admin_get_catalog',
        data: {catalog_val: get_catalog_val},
        contentType: "application/x-www-form-urlencoded",
        success: function (data) {
            if (data == 1) {
                Alert_common('.profile-content', 'warning', '更新失败！', 'warning');
            } else {
                var html = ''
                catalog = 'catalog'
                var item = data['data']
                for (let i = 0; i < item.length; i++) {
                    html = '<tr>\n' +
                        '                                            <td> ' + i + 1 + '</td>\n' +
                        '                                            <td> ' + item[i]["catalog_name"] + ' </td>\n' +
                        '                                            <td>' + item[i]["catalog_since"] + '</td>\n' +
                        '                                            <td>\n' +
                        '                                                <a class="edit" href="/manage/admin_edit_catalog/' + item[i]["id"] + '?select=' + get_catalog_val + '">Edit </a>\n' +
                        '                                            </td>\n' +
                        '                                            <td>\n' +
                        '                                                <a class="delete" onclick="show_delete_modal(' + "catalog" + ',' + item[i]["id"] + ')">Delete </a>\n' +
                        '                                            </td>\n' +
                        '                                        </tr>'
                }
                $('#catalog_table').empty();
                $('#catalog_table').append(html);
            }
        }
    });
}
