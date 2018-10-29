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
        data: {ajax_item_id: JSON.stringify(get_param)},
        url: '/manage/ajax_get_item',
        contentType: "application/json; charset=utf-8",
        //contentType: "application/json",
        dataType: "json",
        success: function (data) {
            console.log(data);
        }
    });
    console.log(get_param);

}