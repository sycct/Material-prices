$(function () {
    $('#user_profile').click(function (event) {
        event.preventDefault();  //prevent the actual form post
        user_profile();
    });

    $('#change_password').click(function (event) {
        event.preventDefault();
        change_password();
    });

    $('#upload_file').click(function (event) {
        event.preventDefault();
        upload_file();
    });

    TableDatatablesEditable.init();

    // Inject our CSRF token into our AJAX request.
    var csrftoken = $('meta[name=csrf-token]').attr('content')

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    })
})

function user_profile() {
    $.ajax({
        type: $('#tab_1_1 form').attr("method"),
        url: $('#tab_1_1 form').attr("action"),
        data: $('#tab_1_1 form').serialize(),
        contentType: "application/x-www-form-urlencoded",
        success: function (data) {
            if (data == 0) {
                Alert_common('.profile-content', 'success', '更新成功！', 'check');
            } else {
                Alert_common('.profile-content', 'warning', '更新失败！', 'warning');
            }
        }
    })
}

function change_password() {
    $.ajax({
        type: $('#tab_1_3 form').attr("method"),
        url: $('#tab_1_3 form').attr("action"),
        data: $('#tab_1_3 form').serialize(),
        contentType: "application/x-www-form-urlencoded",
        success: function (data) {
            if (data == 0) {
                Alert_common('.profile-content', 'success', '更新成功！', 'check');
            } else {
                Alert_common('.profile-content', 'warning', '更新失败！', 'warning');
            }
        }
    })
}

function upload_file() {
    var formData = new FormData();
    formData.append("file", $('#ingredient_file')[0].files[0])
    // add assoc key values, this will be posts values
    $.ajax({
        type: $('#tab_1_2 form').attr("method"),
        url: $('#tab_1_2 form').attr("action"),
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
            if (data == 0) {
                Alert_common('.profile-content', 'success', '更新成功！', 'check');
            } else {
                Alert_common('.profile-content', 'warning', '更新失败！', 'warning');
            }
        }
    })
}

function Alert_common(container, type, message, ico) {
    App.alert({
        container: $(container), // alerts parent container(by default placed after the page breadcrumbs)
        place: 'prepend', // append or prepent in container
        type: type,  // alert's type
        message: message,  // alert's message
        close: true, // make alert closable
        reset: true, // close all previouse alerts first
        focus: true, // auto scroll to the alert after shown
        closeInSeconds: 0, // auto close after defined seconds
        icon: ico // put icon before the message
    });
}

function delete_item(url, id) {
    $.ajax({
        type: 'POST',
        url: url + id,
        success: function (data) {
            if (data == 0) {
                $('#responsive').modal('hide')
                Alert_common('.classification_list', 'success', '删除成功！', 'check');
            } else {
                $('#responsive').modal('hide')
                Alert_common('.classification_list', 'warning', '删除失败！', 'warning');
            }
        }
    })
}

function show_delete_modal(flag, id) {
    $('#responsive').modal('show')
    $('#delete_modal_clse').click(function () {
        $('#responsive').modal('hide')
    })
    var url = '';
    switch (flag) {
        case "catalog":
            url = '/manage/admin_delete_catalog/';
            break;
        case "classification":
            url = '/manage/admin_delete_classification/';
            break;
        case "item":
            url = '/manage/admin_delete_item/';
            break;
    }
    $('#delete_item').click(function () {
        delete_item(url, id);
    })
}

var TableDatatablesEditable = function () {

    var handleTable = function () {

        function restoreRow(oTable, nRow) {
            var aData = oTable.fnGetData(nRow);
            var jqTds = $('>td', nRow);

            for (var i = 0, iLen = jqTds.length; i < iLen; i++) {
                oTable.fnUpdate(aData[i], nRow, i, false);
            }

            oTable.fnDraw();
        }

        function editRow(oTable, nRow) {
            var aData = oTable.fnGetData(nRow);
            var jqTds = $('>td', nRow);
            jqTds[1].innerHTML = '<input type="text" class="form-control input-small" value="' + aData[1] + '">';
            jqTds[2].innerHTML = '<div class="fileinput fileinput-new" data-provides="fileinput">\n' +
                '                                                        <span class="btn green btn-file">\n' +
                '                                                            <span class="fileinput-new"> Select file </span>\n' +
                '                                                            <span class="fileinput-exists"> Change </span>\n' +
                '                                                            <input type="file" name="edit_classification_icon" id="edit_classification_icon"> </span>\n' +
                '                                                        <span class="fileinput-filename"> </span> &nbsp;\n' +
                '                                                        <a href="javascript:;" class="close fileinput-exists" data-dismiss="fileinput"> </a>\n' +
                '                                                    </div>';
            jqTds[3].innerHTML = '<a class="edit" href="javascript:;">Save</a>';
            jqTds[4].innerHTML = '<a class="cancel" href="">Cancel</a>';
        }

        function saveRow(oTable, nRow) {
            var jqInputs = $('input', nRow);
            oTable.fnUpdate(jqInputs[0].value, nRow, 1, false);
            oTable.fnUpdate(jqInputs[1].value, nRow, 2, false);
            oTable.fnUpdate('<a class="edit" href="">Edit</a>', nRow, 3, false);
            oTable.fnUpdate('<a class="delete" href="">Delete</a>', nRow, 4, false);
            oTable.fnDraw();
        }

        function cancelEditRow(oTable, nRow) {
            var jqInputs = $('input', nRow);
            oTable.fnUpdate(jqInputs[0].value, nRow, 0, false);
            oTable.fnUpdate(jqInputs[1].value, nRow, 1, false);
            oTable.fnUpdate(jqInputs[2].value, nRow, 2, false);
            oTable.fnUpdate(jqInputs[3].value, nRow, 3, false);
            oTable.fnUpdate('<a class="edit" href="">Edit</a>', nRow, 4, false);
            oTable.fnDraw();
        }

        var table = $('#sample_editable_1');

        var oTable = table.dataTable({

            // Uncomment below line("dom" parameter) to fix the dropdown overflow issue in the datatable cells. The default datatable layout
            // setup uses scrollable div(table-scrollable) with overflow:auto to enable vertical scroll(see: assets/global/plugins/datatables/plugins/bootstrap/dataTables.bootstrap.js).
            // So when dropdowns used the scrollable div should be removed.
            //"dom": "<'row'<'col-md-6 col-sm-12'l><'col-md-6 col-sm-12'f>r>t<'row'<'col-md-5 col-sm-12'i><'col-md-7 col-sm-12'p>>",

            "lengthMenu": [
                [5, 15, 20, -1],
                [5, 15, 20, "All"] // change per page values here
            ],

            // Or you can use remote translation file
            //"language": {
            //   url: '//cdn.datatables.net/plug-ins/3cfcc339e89/i18n/Portuguese.json'
            //},

            // set the initial value
            "pageLength": 5,

            "language": {
                "lengthMenu": " _MENU_ records"
            },
            "columnDefs": [{ // set default column settings
                'orderable': true,
                'targets': [0]
            }, {
                "searchable": true,
                "targets": [0]
            }],
            "order": [
                [0, "asc"]
            ] // set first column as a default sort by asc
        });

        var tableWrapper = $("#sample_editable_1_wrapper");

        var nEditing = null;
        var nNew = false;

        $('#sample_editable_1_new').click(function (e) {
            e.preventDefault();

            if (nNew && nEditing) {
                if (confirm("Previose row not saved. Do you want to save it ?")) {
                    saveRow(oTable, nEditing); // save
                    $(nEditing).find("td:first").html("Untitled");
                    nEditing = null;
                    nNew = false;

                } else {
                    oTable.fnDeleteRow(nEditing); // cancel
                    nEditing = null;
                    nNew = false;

                    return;
                }
            }

            var aiNew = oTable.fnAddData(['', '', '', '', '', '']);
            var nRow = oTable.fnGetNodes(aiNew[0]);
            editRow(oTable, nRow);
            nEditing = nRow;
            nNew = true;
        });

        table.on('click', '.delete', function (e) {
            e.preventDefault();

            if (confirm("Are you sure to delete this row ?") == false) {
                return;
            }

            var nRow = $(this).parents('tr')[0];
            oTable.fnDeleteRow(nRow);
            alert("Deleted! Do not forget to do some ajax to sync with backend :)");
        });

        table.on('click', '.cancel', function (e) {
            e.preventDefault();
            if (nNew) {
                oTable.fnDeleteRow(nEditing);
                nEditing = null;
                nNew = false;
            } else {
                restoreRow(oTable, nEditing);
                nEditing = null;
            }
        });

        table.on('click', '.edit', function (e) {
            e.preventDefault();

            /!* Get the row as a parent of the link that was clicked on *!/
            var nRow = $(this).parents('tr')[0];

            if (nEditing !== null && nEditing != nRow) {
                /!* Currently editing - but not this row - restore the old before continuing to edit mode *!/
                restoreRow(oTable, nEditing);
                editRow(oTable, nRow);
                nEditing = nRow;
            } else if (nEditing == nRow && this.innerHTML == "Save") {
                /!* Editing this row and want to save it *!/
                saveRow(oTable, nEditing);
                nEditing = null;
                alert("Updated! Do not forget to do some ajax to sync with backend :)");
            } else {
                /!* No edit in progress - let's start one *!/
                editRow(oTable, nRow);
                nEditing = nRow;
            }
        });
    }

    return {

        //main function to initiate the module
        init: function () {
            handleTable();
        }

    };

}();

var check_select = function () {
    // get to link select element
    var get_select_val = loadPageVar("select")
    if (get_select_val.replace(/(^s*)|(s*$)/g, "").length == 0) {
        return false;
    }
    $('#Catalog_to_Classification option').each(function () {
        if ($(this).val() == get_select_val) {
            $(this).attr('selected', 'selected');
        }
    })
}();

function loadPageVar(sVar) {
    return decodeURI(window.location.search.replace(new RegExp("^(?:.*[&\\?]" + encodeURI(sVar).replace(/[\.\+\*]/g, "\\$&") + "(?:\\=([^&]*))?)?.*$", "i"), "$1"));
}
