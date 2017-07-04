window.Superlists = {}
window.Superlists.hide_on_keypress = function() {
    $('input[name="text"]').on('keypress', function() {
        $('.has-error').hide();
    });
};
