var ComponentsBootstrapSelectSplitter = function() {

    var selectSplitter = function() {
        $('#select_selectsplitter1').selectsplitter({
            selectSize: 4
        });
    }

    return {
        //main function to initiate the module
        init: function() {
            selectSplitter();
        }
    };

}();

jQuery(document).ready(function() {    
   ComponentsBootstrapSelectSplitter.init(); 
});