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
                html = ''
                $.each(data, function (index, value) {
                    html = '<tr>\n' +
                        '                                            <td> ' + index + '</td>\n' +
                        '                                            <td> ' + value.catalog_name + ' </td>\n' +
                        '                                            <td>' + value.catalog_since + '</td>\n' +
                        '                                            <td>\n' +
                        '                                                <a class="edit" href="{{ url_for(\'.admin_edit_catalog\', id=item.id) }}">Edit </a>\n' +
                        '                                            </td>\n' +
                        '                                            <td>\n' +
                        '                                                <a class="delete" onclick="show_delete_modal()">Delete </a>\n' +
                        '                                            </td>\n' +
                        '                                        </tr>'
                })
                $('#catalog_table').append(html);
            }
        }
    });
}

