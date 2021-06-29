/* register widget initialization for a formset form */
var DEBUG = true;
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
        var formset_form = $checkbox.closest(".formset-form");

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
        //cheaking an upstear item 
        revise_clonable_select(modal_content.parents(".modal"), revise_clonable_select);
    });
}

function invoke_modal_window(modal_window, response, cur_select) {
    //alert(modal_window);
    //modal_window.modal();
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
        modal_window.modal('hide');
        modal_dynamic_content.html("");
    });

    modal_window.on("shown.bs.modal", function () {
        console.log("shown.bs.modal");
        let items = modal_window.find(".address-item");
        if (items.length > 0) {
            console.log("there're some items");
        } else {
            cur_select.clone()
                .show()
                .attr("id", cur_select.attr("id") + "-clone")
                .addClass("clonable")
                .insertAfter(".formset-forms:last");
            let select_autocomplete = create_select2_modal_wnd(result_func);
            select_autocomplete(
                "#" + cur_select.attr("id") + "-clone",
                null,
                url_get_address,
                url_post_address
            );
        }
    });
}

function get_formset_forms(wnd) {
    return wnd.find(".formset-forms");
}

function get_clonable_select(wnd) {
    let formset_forms = get_formset_forms(wnd);
    let formset_form = formset_forms.find(".formset-form");
    let formset_form_last = formset_form.last();
    if (formset_form_last.length == 1) {
        let clonable_select = formset_form_last.find(".clonable");
        if (clonable_select.length == 1) {
            return clonable_select;
        }
    }
    return null;
}

function is_selected_above_item(wnd) {
    let formset_forms = get_formset_forms(wnd);
    let formset_forms_list = formset_forms.find(".formset-form");
    if (formset_forms_list.length > 0) {
        let select = formset_form_last.find("select").last();
        return select.val() != "";
    }
    else {
        return false;
    }
}

function revise_clonable_select(wnd, is_selected_above_item) {
    let clonable_select = get_clonable_select(wnd);
    if (clonable_select != null && is_selected_above_item != null) {
        if (is_selected_above_item()) {
            clonable_select.attr("disabled", "true");
        }
        else {
            clonable_select.attr("disabled", "false");
        }
    } else {
        if (DEBUG) {
            console.log("get_clonable_select hasn't found by revise_clonable_select");
        }
    }
}



$(function () {
    let cur_select = null;
    var modal_window = $(document).find(".modal");
    var modal_dynamic_content = modal_window.find(".modal-dynamic-content");
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
        $(this).on('click', function (e) {
            console.log(e + ": " + $(this).text());
            let uri = $(this).attr('action');
            let address_modal_wnd = uri.replaceAll('/', '') + "_modal_wnd";
            let parent_form_group = $(this).closest(".form-group");
            cur_select = parent_form_group.find("select").eq(0);

            e.preventDefault();
            uri += cur_select.val();
            console.log(uri);
            $.ajax({
                url: uri,
                method: "GET",
                //data: { id: menuId },
                dataType: "html"
            }).done(function (data) {
                let modal_window = $('#' + address_modal_wnd);
                invoke_modal_window(modal_window, data, cur_select);
            }).fail(function () {
                console.log("error");
            }).always(function () {
                console.log('always')
            });

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
                invoke_modal_window($(document), data);
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
    $('.btn-primary').click(function () {
        console.log('btn-primary pressed!');

        let current_parent_wnd = cur_select.parent();
        let clonable_select_id = "#" + cur_select.attr("id") + "-clone";
        let clone_select = $(clonable_select_id);
        let test_value = clone_select.val();
        cur_select.val(test_value);
        test_value = cur_select.val();
        modal_window.modal('hide');
        modal_dynamic_content.html("");
    });
});
