(function ($) {

    'use strict';

    const Forms = function () {
        this.$body = $('body');
    };
    // Form Elements
    Forms.prototype.initFormElements = function () {
        const inside = $(".inside");
        // noinspection JSValidateTypes
        inside.children('input').blur(function () {
            $(this).parent().children('.add-on').removeClass('input-focus');
        });
        // noinspection JSValidateTypes
        inside.children('input').focus(function () {
            $(this).parent().children('.add-on').addClass('input-focus');
        });

        const inputTransparent = $(".input-group.transparent");
        // noinspection JSValidateTypes
        inputTransparent.children('input').blur(function () {
            $(this).parent().children('.input-group-addon').removeClass('input-focus');
        });
        // noinspection JSValidateTypes
        inputTransparent.children('input').focus(function () {
            $(this).parent().children('.input-group-addon').addClass('input-focus');
        });

        const bootstrapTags = $(".bootstrap-tagsinput input");
        bootstrapTags.blur(function () {
            $(this).parent().removeClass('input-focus');
        });

        bootstrapTags.focus(function () {
            $(this).parent().addClass('input-focus');
        });
    };
    // Validation Plugin
    Forms.prototype.initValidatorPlugin = function () {
        $.validator && $.validator.setDefaults({
            errorPlacement: function (error, element) {
                const parent = $(element).closest('.form-group');
                if (parent.hasClass('form-group-default')) {
                    parent.addClass('has-error');
                    error.insertAfter(parent);
                } else {
                    error.insertAfter(element);
                }
            },
            onfocusout: function (element) {
                const parent = $(element).closest('.form-group');
                if ($(element).valid()) {
                    parent.removeClass('has-error');
                    parent.next('.error').remove();
                }
            },
            onkeyup: function (element) {
                const parent = $(element).closest('.form-group');
                if ($(element).valid()) {
                    $(element).removeClass('error');
                    parent.removeClass('has-error');
                    parent.next('label.error').remove();
                    parent.find('label.error').remove();
                } else {
                    parent.addClass('has-error');
                }
            }
        });

        $('.validate').validate();
    };
    Forms.prototype.init = function () {
        // init layout
        this.initFormElements();
        this.initValidatorPlugin();

    };

    $.Forms = new Forms();
    $.Forms.Constructor = Forms;

})(window.jQuery);


$(function () {
    'use strict';
    // Initialize layouts and plugins
    $.Forms.init();
});