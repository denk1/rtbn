/* register widget initialization for a formset form */
var DEBUG = true;
var cur_select = null;
window.WIDGET_INIT_REGISTER = window.WIDGET_INIT_REGISTER || [];
var tree_modal_window = $("#tree_modal_wnd");

var pathes = null;

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
}

function invoke_modal_window(modal_window, response, cur_select) {
    var modal_dynamic_content = modal_window.find(".modal-dynamic-content");
    modal_dynamic_content.html(response + modal_dynamic_content.html());
    //modal_window.modal('show');
    init_warunit_form(modal_dynamic_content);
}

function get_formset_forms(wnd) {
    return wnd.find(".formset-forms");
}

function get_clonable_select(wnd) {

    let clonable_select = wnd.find(".clonable");
    if (clonable_select.length == 1) {
        return clonable_select;
    }
    return null;
}

function is_selected_above_item(wnd) {
    let formset_forms = get_formset_forms(wnd);
    let formset_forms_list = formset_forms.find(".formset-form").not(".d-none");
    if (formset_forms_list.length > 0) {
        let select = formset_forms_list.find("select").last();
        console.log("formset_forms_list.length=", formset_forms_list.length);
        console.log("select.val() is ", select.val());
        return select.val() === "";
    }
    else {
        return false;
    }
}

function revise_clonable_select(wnd, is_selected_above_item) {
    let clonable_select = get_clonable_select(wnd);
    if (clonable_select != null && is_selected_above_item != null) {
        let is_item = is_selected_above_item(wnd);
        console.log("the result is ", is_item);
        if (is_item) {
            clonable_select.attr("disabled", true);
            console.log("set true");
        }
        else {
            clonable_select.attr("disabled", false);
            console.log("set false");
        }
    } else {
        if (DEBUG) {
            console.log("get_clonable_select hasn't found by revise_clonable_select");
        }
    }
}

function hidden_bs_modal() {
    var modal_dynamic_content = tree_modal_window.find(".modal-dynamic-content");
    modal_dynamic_content.html("");
}


function InitSelect2() {
    this.wnd = null;
    this.m_cur_clone_select = null;
    this.init_autocomplete = function (select_widget) {
        var pathes = addressUrls;
        let check_count = select_widget.hasClass("clonable") ? 0 : 1;
        let select_autocomplete = new create_select2_modal_wnd(result_func);
        let parent_length = get_formset_forms(this.wnd).find(".formset-form").not(".d-none").length;
        let parent_element = null;
        if (select_widget.hasClass("clonable")) {
            parent_element = parent_length == check_count ? null : get_formset_forms(this.wnd)
                .find(".formset-form")
                .not(".d-none")
                .last()
                .find("select");
        }
        else {
            parent_element = select_widget.parents(".formset-form").prev().find("select");
        }
        if (select_widget.hasClass("select2-hidden-accessible")) {
            select_widget.select2('destroy').off('select2:select');
            //select_widget.data('select2').destroy();
            console.log('destroy');
        }
        select_autocomplete.select_autocomplete(
            select_widget,
            parent_element,
            pathes.get_data_url,
            pathes.get_source_url
        );
        //select_widget.select2('destroy');
    }

    this.init_select2_clonable = function ($current_element) {
        let cur_clon_select = cur_select.clone(true)
            .show()
            .attr("id", cur_select.attr("id") + "-clone")
            .addClass("clonable")
            .insertAfter(".formset-forms:last");
        this.m_cur_clone_select = cur_clon_select;
        this.init_autocomplete(cur_clon_select);
        console.log("cur_select.val=" + cur_select.val());
        this.m_cur_clone_select.val(cur_select.val()).trigger('change');

    }

    this.change_parent_clonable_item = function () {
        if (this.m_cur_clone_select != null)
            this.init_autocomplete(this.m_cur_clone_select);
        else
            console.log("the clonable select is null");
    }
}

function init_select2_list(init_obj) {
    if (init_obj.wnd != null) {
        let $formset_forms_list = get_formset_forms(init_obj.wnd).find(".formset-form");
        $formset_forms_list.each(function () {
            let select = $(this).find("select");
            init_obj.init_autocomplete(select);
            console.log(select);
        });
    }
}

var init_select2 = new InitSelect2();

function revise_tree_units(items) {
    $(items[0]).find("select").attr("disabled", false);
    for (let i = 1; i < items.length; i++) {
        if ($(items[i - 1]).find("select").children("option:selected").val() === "")
            $(items[i]).find("select").attr("disabled", true);
        else
            $(items[i]).find("select").attr("disabled", false);
        console.log($(items[i]).find("select").children("option:selected").val());
    }
}

function get_list_tree_units(wnd) {
    let items = get_formset_forms(wnd).find(".formset-form").not(".d-none");
    console.log("the length of formsets is " + items.length);
    revise_tree_units(items);
}



function Foo(i) {
    console.log(i);
}

$(function () {
    //tree_modal_window = init_modal_wnd();
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
                invoke_modal_window($("#tree_modal_wnd"), data, cur_select);
                init_select2.wnd = $("#tree_modal_wnd");
                init_select2.init_select2_clonable($("#tree_modal_wnd"));
                init_select2_list(init_select2);

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
        $formset.addClass("d-none");
        console.log("click delete");
        get_list_tree_units($(this).parents(".modal"));
        //$formset.hide();
    });
    $(document).on('click', '#address_section .delete', function (e) {
        console.log(e.target);
        e.preventDefault();
        var modal_wnd = $(this).parents(".modal");
        if (modal_wnd.length == 1) {
            revise_clonable_select(modal_wnd, is_selected_above_item);
        } else {
            console.log("Something's gone wrong!");
            console.log(" the modal address window is none or multiple");
        }
    });

    $(document).on("shown.bs.modal", "#tree_modal_wnd", function (e) {
        console.log('shown.bs.modal');
        //init_select2.wnd = $(this);
        //init_select2.init_select2_clonable($(this));
    });

    $(document).on("hidden.bs.modal", "#tree_modal_wnd", hidden_bs_modal);

    $('.btn-primary').click(function () {
        console.log('btn-primary pressed!');
        let clonable_select_id = "#" + cur_select.attr("id") + "-clone";
        let clone_select = $(clonable_select_id);
        let test_value = clone_select.val();
        let $options = clone_select.find("option").clone();
        cur_select
            .find("option")
            .remove()
            .end()
            .append($options)
            .val(test_value);

        modal_window.modal('hide');
        modal_dynamic_content.html("");
    });

    $(document).on("click", ".add-tree-form", function (e) {
        pathes = addressUrls;
        e.preventDefault();
        let $formset = $(this).closest('.formset');
        let wnd = $formset.parents(".modal");
        var $total_forms = $formset.find('[id$="TOTAL_FORMS"]');
        let empty_form = $formset.find('.empty-warunit-form');
        var $new_form = empty_form.clone(true).attr("id", null);
        $new_form.removeClass('empty-warunit-form d-none').addClass('formset-form');
        set_index_for_fields($new_form, parseInt($total_forms.val(), 10));
        $formset.find('.formset-forms').append($new_form);
        add_delete_button($new_form);
        $total_forms.val(parseInt($total_forms.val(), 10) + 1);
        reinit_widgets($new_form);
        init_select2.wnd = wnd;
        init_select2.init_autocomplete($new_form.find("select"));
        init_select2.change_parent_clonable_item();
        //cheaking an upstear item 
        revise_clonable_select(wnd, is_selected_above_item);
        get_list_tree_units(wnd);
    });

    $(document).on('change', '.formset-forms select', function (e) {
        console.log("test of change");
        get_list_tree_units($(this).parents(".modal"));
        revise_clonable_select($(this).parents(".modal"), is_selected_above_item);
    });
});
