var ComponentsBootstrapTagsinput = function() {

    var handleDemo1 = function() {
        var elt = $('#property_value');
        
        elt.tagsinput({
          itemValue: 'value',
          itemText: 'text',
        });

        $('#object_tagsinput_add').on('click', function(){
            elt.tagsinput('add', {
                "value": $('#object_tagsinput_value').val(),
                "text": $('#object_tagsinput_value').val(),
            });
        });
    }


    return {
        //main function to initiate the module
        init: function() {
            handleDemo1();
        }
    };

}();

jQuery(document).ready(function() {
    ComponentsBootstrapTagsinput.init();
});