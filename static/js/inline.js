/* register widget initialization for a formset form */
window.WIDGET_INIT_REGISTER = window.WIDGET_INIT_REGISTER || [];

function reinit_widgets($formset_form) {
    $(window.WIDGET_INIT_REGISTER).each(function (index, func) {
        func($formset_form);
    });
}

function set_index_for_fields($formset_form, index) {
    $formset_form.find(':input').each(function () {
        var $field = $(this);
        if ($field.attr("id")) {
            $field.attr(
                "id",
                $field.attr("id").replace(/-__prefix__-/, "-" + index + "-")
            );
        }
        if ($field.attr("name")) {
            $field.attr(
                "name",
                $field.attr("name").replace(/-__prefix__-/, "-" + index + "-")
            );
        }
    });
    $formset_form.find('label').each(function () {
        var $field = $(this);
        if ($field.attr("for")) {
            $field.attr(
                "for",
                $field.attr("for").replace(/-__prefix__-/, "-" + index + "-")
            );
        }
    });
    $formset_form.find('div').each(function () {
        var $field = $(this);
        if ($field.attr("id")) {
            $field.attr(
                "id",
                $field.attr("id").replace(/-__prefix__-/, "-" + index + "-")
            );
        }
    });
}

function add_delete_button($formset_form) {
    $formset_form.find('input:checkbox[id$=DELETE]').each(function () {
        var $checkbox = $(this);
        var $deleteLink = $(
            '<button class="delete btn btn-sm btn-danger mb-3">Remove</button>'
        );
        var formset_form =$checkbox.closest(".formset-form");

        formset_form.append($deleteLink);
        $checkbox.closest('.form-group').hide();
    });
}

function init_warunit_form(modal_content) {
    var formset = modal_content.find(".formset-form");
    add_delete_button(formset);
    $('.add-warunit-form').click(function (e) {
        e.preventDefault();
        var $formset = $(this).closest('.formset');
        var $total_forms = $formset.find('[id$="TOTAL_FORMS"]');
        var $new_form = $formset.find('.empty-warunit-form').clone(true).attr("id", null);
        $new_form.removeClass('empty-warunit-form d-none').addClass('formset-form');
        set_index_for_fields($new_form, parseInt($total_forms.val(), 10));
        $formset.find('.formset-forms').append($new_form);
        add_delete_button($new_form);
        $total_forms.val(parseInt($total_forms.val(), 10) + 1);
        reinit_widgets($new_form);
    });
}

function invoke_modal_window(formset, response) {
    var modal_window = formset.find(".modal");
    //alert(modal_window);
    modal_window.modal();
    modal_window.modal({
        'show': true,
        'focus': true,
        'keyboard': true
    });
    
    var modal_dynamic_content = modal_window.find(".modal-dynamic-content");
    modal_dynamic_content.html(response + modal_dynamic_content.html());
    modal_window.modal('show');
    init_warunit_form(modal_dynamic_content);
    modal_window.on("hidden.bs.modal", function () {
        modal_dynamic_content.html("");
    });
}

$(function () {

    $('.add-inline-form').click(function (e) {
        e.preventDefault();
        var $formset = $(this).closest('.formset');
        var $total_forms = $formset.find('[id$="TOTAL_FORMS"]');
        var $new_form = $formset.find('.empty-form').clone(true).attr("id", null);
        $new_form.removeClass('empty-form d-none').addClass('formset-form');
        set_index_for_fields($new_form, parseInt($total_forms.val(), 10));
        $formset.find('.formset-forms').append($new_form);
        add_delete_button($new_form);
        $total_forms.val(parseInt($total_forms.val(), 10) + 1);
        reinit_widgets($new_form);
    });
    $('.formset-form').each(function () {
        $formset_form = $(this);
        add_delete_button($formset_form);
        reinit_widgets($formset_form);
    });
    $('.invoke-modal').each(function () {
        $war_unit = $(this);
        $war_unit.on('click', function (e) {
            e.preventDefault();
        });
    });
    $('.btn-unit').each(function () {
        war_unit = $(this);
        war_unit.on('click', function (e) {
            e.preventDefault();
            var cur_form = $(this).parents(".formset-form");
            var modal_window = cur_form.find(".modal-body")
            var cur_select_text = modal_window.find(":selected").text();
            var cur_select_val = modal_window.find(":selected").val();
            $.ajax({
                url: "/military_unit/" + cur_select_val,
                method: "GET",
                //data: { id: menuId },
                dataType: "html"
            }).done(function (data) {
                console.log("Sample of data:", data);
                invoke_modal_window(cur_form, data);
            }).fail(function () {
                console.log("error");
            }).always(function () {
                console.log('always')
            });

        });
    });
    $(document).on('click', '.delete', function (e) {
        e.preventDefault();
        var $formset = $(this).closest('.formset-form');
        var $checkbox = $formset.find('input:checkbox[id$=DELETE]');
        $checkbox.attr("checked", "checked");
        $formset.hide();
    });
});
