$(document).ready(function () {
    $('.increment-btn').click(function(e) {
        e.preventDefault();
        var inc_value = $(this).closest('.cart_item').find('.qty-input').val();
        var value = parseInt(inc_value,10);
        value = isNan(value) ? 0 :value ;
        if (value < 10){
            value++;
            $(this).closest('.cart_item').find('.qty-input').val(value);
        }

    });

});