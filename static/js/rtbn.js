function set_disabled_input(v, r, d, l) {
    if (v) {
        r.disabled = true;
        d.disabled = true;
        l.disabled = true;
        r.required = false;
        d.required = false;
        l.required = false;
        r.value = "";
        d.value = "";
        l.value = "";

    } else {
        r.disabled = false;
        d.disabled = false;
        l.disabled = false;
        r.required = true;
        d.required = true;
        l.required = true;
    }
}

function creation_tag(tag) {
    return {
        id: tag.term,
        text: tag.term,
        tag: true
    };
}

function selection_choisen(cur_item, evt, type_item, parent_item, url_post) {
    var parent_val = null;
    if (parent_item != null && parent_item.length != 0) {
        parent_val = $(parent_item).val();
    }

    if ((evt.params.data.tag == true)) {
        console.log(evt.params.data);
        $.ajax({
            url: url_post,
            dataType: 'json',
            data: {
                id: evt.params.data.id,
                text: evt.params.data.text,
                tag: evt.params.data.tag,
                selected: evt.params.data.selected,
                type_item: type_item,
                parent_item: parent_val
            },
            method: "POST",
            success: function (data) {
                //alert('test');
                //response(data);
                console.log(data);
            },
            error: function (error) {

            },

        }).done(function (response) {
            evt.params.data.id = response.id;
            for (var i = 0; i < evt.target.length; i++) {

                if (evt.target[i].getAttribute("data-select2-tag")) {
                    console.log(evt.target[i].getAttribute("data-select2-tag"));
                    evt.target[i].value = response.id;
                    console.log(evt.target[i]);
                }
            }
        }).fail(function () {
            console.log('fail');
        }).always(function () {
            console.log('always');
        });
    }
}

function result_func(item) {
    return { id: item.id, text: item.address_item_name };
}

function result_enlistment_office(item) {
    return { id: item.id, text: item.name };
}

function result_warunit(item) {
    return { id: item.id, text: item.name };
}

function create_set_select2_item(result_func) {
    return function (item_name, type_item, parent_item, url_get, url_post) {
        item = $(item_name)
        $(item).select2({
            tags: true,
            tokenSeparators: [",", " "],
            createTag: creation_tag,
            ajax: {
                url: url_get,
                dataType: 'json',
                method: 'post',
                params: { // extra parameters that will be passed to ajax
                    contentType: "application/json; charset=utf-8",
                },
                data: function (term, page) {
                    if (parent_item == null) {
                        query_item = {
                            term: term.term,
                            type_item: type_item,
                        };
                    } else {

                        query_item = {
                            term: term.term,
                            type_item: type_item,
                            parent_id: $(parent_item).val()
                        };
                    }
                    return query_item;
                },
                processResults: function (data) {
                    return {
                        results: $.map(data, result_func)
                    }
                }
            }
        }).on('select2:select', function (evt) {
            selection_choisen(item, evt, type_item, parent_item, url_post);
        });
    }
}

function create_select2_modal_wnd(result_func) {
    this.select_autocomplete = function (item, parent_item_in, url_get, url_post) {
        var parent_item = parent_item_in;
        item.select2({
            tags: true,
            tokenSeparators: [","],
            createTag: creation_tag,
            selectionCssClass: "form-control select2-allow-clear",
            //dropdownCssClass: "select2-selection select2-selection--single",
            theme: 'bootstrap4',
            ajax: {
                url: url_get,
                dataType: 'json',
                method: 'post',
                params: { // extra parameters that will be passed to ajax
                    contentType: "application/json; charset=utf-8",
                },
                data: function (term, page) {
                    if (parent_item == null || $(parent_item).val() === null || $(parent_item).val() === "") {
                        query_item = {
                            term: term.term
                        };
                    } else {

                        query_item = {
                            term: term.term,
                            parent_id: $(parent_item).val()
                        };
                    }
                    return query_item;
                },
                processResults: function (data) {
                    return {
                        results: $.map(data, result_func)
                    }
                }
            }
        }).on('select2:select', function (evt) {
            selection_choisen(item, evt, null, parent_item, url_post);
        });
    }
}

let url_get_address = null;
let url_post_address = null;
function set_url_address(url_get, url_post) {
    url_get_address = url_get;
    url_post_address = url_post;
}