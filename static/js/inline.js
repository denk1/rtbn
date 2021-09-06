/* register widget initialization for a formset form */
var DEBUG = true;
var cur_select = null;
var $cur_btn_tree = null;
window.WIDGET_INIT_REGISTER = window.WIDGET_INIT_REGISTER || [];
var tree_modal_window = $("#tree_modal_wnd");

var pathes = null,
    func_result = null,
    pathes_obj = null;

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

function create_get_ajax_request(uri, do_this) {
    return function () {
        $.ajax({
            url: uri,
            method: "GET",
            //data: { id: menuId },
            dataType: "html"
        }).done(
            do_this
        ).fail(function () {
            console.log("error");
        }).always(function () {
            console.log('always')
        });
    }
}

function init_btn_primary(wnd, uri) {
    let btn_primary = wnd.find(".btn-primary");
    btn_primary.attr("action", uri);
}

function get_btn_primary_action(btn) {
    return btn.attr("action");
}

function init_btn_box_inform(btn, select, uri) {
    let get_ajax_request = create_get_ajax_request(uri, function (data) {
        let str_val = "";
        console.log(str_val);
        let selects = $(data)
            .find(".formset-forms")
            .find("select")
            .not("d-none");
        selects.each(function (item) {
            let str = $(this).find("option:selected").text().split(" ")[1];
            if (typeof str !== "undefined")
                str_val += $(this).find("option:selected").text().split(" ")[1] + ", ";
        });
        str_val += select.find("option:selected").text();
        if (btn != null) {
            console.log("cur_btn_tree");
            console.log($cur_btn_tree.prev(".inform-box-label").text(str_val));
        }
    });
    get_ajax_request();
}

function init_btn_war_unit() {
    let $paragraph_inform_box = $("<p class='inform-box-label'></p>");
    let $button_war_unit = $(`<input type="button" name="war_unit_button"
                            value="Подразделение"
                            class="btn input-block-level btn-unit invoke-modal"
                            data-toggle="modal" 
                            data-target="#tree_modal_wnd" 
                            action="/war_unit/">`);
    let div_inform_box = $('<div></div>')
        .addClass("inform-box")
        .append($paragraph_inform_box)
        .append($button_war_unit);

    let test_element = $(".hidden-select")
        .parent()
        .addClass("d-none")
        .parent()
        .append(div_inform_box);

    console.log(test_element);
}

function init_btn_address_item() {
    let $paragraph_inform_box = $("<p class='inform-box-label'></p>");
    let $button_war_unit = $(`<input type="button" name="address_item_button"
                            value="Адрес"
                            class="btn input-block-level btn-address invoke-modal"
                            data-toggle="modal" 
                            data-target="#tree_modal_wnd" 
                            action="/address/">`);
    let div_inform_box = $('<div></div>')
        .addClass("inform-box")
        .append($paragraph_inform_box)
        .append($button_war_unit);

    let test_element = $(".hidden-select-address")
        .parent()
        .addClass("d-none")
        .parent()
        .append(div_inform_box);

    console.log(test_element);
}



function init_action_btns() {
    let address = $(".btn-address").attr("action");
    let war_unit = $(".btn-unit").attr("action");

    pathes_obj = { [address]: addressUrls, [war_unit]: war_unitUrs };
    change_depended_select($("#id_military_enlistment_office_address"), $("#id_military_enlistment_office"));
}

function change_depended_select($element_checked, $purpose_element) {
    if ($element_checked.val() === null || $element_checked.val() === "") {
        $purpose_element
            .val("")
            .trigger("change")
            .attr("disabled", true);

    } else {
        $purpose_element
            .attr("disabled", false);
    }

    console.log("change!");
}

function init_select_by_name($btn, class_name, urls) {
    let $formset = $btn.closest('.formset');
    let $selects = $formset.find(".formset-forms ." + class_name);
    let select_autocomplete = new create_select2_modal_wnd(result_func);
    $selects.each(function () {
        console.log($(this));

        if ($(this).hasClass("select2-hidden-accessible")) {
            $(this)
                .empty()
                .select2("destroy")
                .off('select2:select');
                console.log("destroy");
            }
    });
    select_autocomplete.select_autocomplete($selects, null, urls.get_data_url, urls.get_source_url);
}

function init_datetime_picker($btn) {
    let $formset = $btn.closest('.formset');
    $formset.find(".dateinput")
        .datepicker("destroy")
        .datepicker();

}
 
$(function () {
    //tree_modal_window = init_modal_wnd();
    var modal_window = $(document).find(".modal");
    var modal_dynamic_content = modal_window.find(".modal-dynamic-content");
    init_btn_war_unit();
    init_action_btns();
    init_btn_address_item();
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

    $('.invoke-modal')
        .on('click', function (e) {
            $cur_btn_tree = $(this);
            console.log(e + ": " + $(this).text());
            let uri = $(this).attr('action');
            pathes = pathes_obj[uri];
            let parent_form_group = $(this).closest(".form-group");
            cur_select = parent_form_group.find("select").eq(0);
            var modal_wnd = $("#tree_modal_wnd");
            init_btn_primary(modal_wnd, uri);
            e.preventDefault();
            if (cur_select.val() != null && typeof cur_select.val() !== 'undefined')
                uri += cur_select.val();
            console.log(uri);
            let get_ajax_request = create_get_ajax_request(uri, function (data) {
                invoke_modal_window(modal_wnd, data, cur_select);
                init_select2.wnd = modal_wnd;
                init_select2.init_select2_clonable(modal_wnd);
                init_select2_list(init_select2);

            });
            get_ajax_request();
        })
        .each(function () {
            let select = $(this).parents(".form-group").find("select");
            if (select.length == 1 && select.val() != "" && select.val() != null) {
                console.log($(this).attr("action"));
                let str_uri = $(this).attr("action") + select.val();
                init_btn_box_inform($(this), select, str_uri);
            }
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

    $('.btn-save').click(function () {
        let clonable_select_id = "#" + cur_select.attr("id") + "-clone";
        let clone_select = $(clonable_select_id);
        let test_value = clone_select.val();
        let $options = clone_select.find("option").clone();
        let str_uri = "";

        if (DEBUG)
            console.log('btn-save pressed!');
        cur_select
            .find("option")
            .remove()
            .end()
            .append($options)
            .val(test_value);

        modal_window.modal('hide');
        modal_dynamic_content.html("");
        str_uri = get_btn_primary_action($(this)) + clone_select.val();
        init_btn_box_inform($cur_btn_tree, cur_select, str_uri);
    });



    $(document).on("click", ".add-tree-form", function (e) {
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

    $("#id_military_enlistment_office_address").on("change", function (e) {
        change_depended_select($(this), $("#id_military_enlistment_office"));
    });

    $()

    $(".btn-unit")
        .attr(
            "data-toggle", "modal"
        )
        .attr(
            "data-target", "#tree_modal_wnd"
        )
        .attr(
            "action", "/war_unit/"
        );

    $('.add-calling-team').click(function (e) {

        e.preventDefault();
        console.log("add-calling-team");
        init_select_by_name($(this), "calling-team", calling_teamUrls);
    });

    $('.add-war-achievement').click( function (e) {
        e.preventDefault();
        console.log("add-war-achievement");
        init_select_by_name($(this), "war-operation", war_operationUrls);
        init_datetime_picker($(this));
    });

    $('.add-hospitalization').click( function (e) {
        e.preventDefault();
        console.log("add-hospitalization");
        init_select_by_name($(this), "hospital", hospitalUrls);
        init_datetime_picker($(this));
    });

    $('.add-captivity').click( function (e) {
        e.preventDefault();
        console.log("add-captivity");
        init_datetime_picker($(this));
    });

    $('.add-being-camped').click(function (e) {
            e.preventDefault();
            console.log(".add-being-camped");
            init_select_by_name($(this), "camp", campUrls);
            init_datetime_picker($(this));
    });

    $('.add-compulsory-work').click(function (e) {
        e.preventDefault();
        console.log("add-compulsory-work");
        init_select_by_name($(this), "labour-team", labour_teamUrls);
        init_datetime_picker($(this));  
    });

    $('.add-infirmary-camp').click(function (e) {
        e.preventDefault();
        console.log("add-infirmary-camp");
        init_select_by_name($(this), "camp", campUrls);
        init_datetime_picker($(this));  
    });
});
