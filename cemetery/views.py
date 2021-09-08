from django.shortcuts import render, redirect, get_object_or_404
from .models import CemeteryItem
from .forms import CemeteryItemForm
from django.forms import modelformset_factory
from common.functions import get_tree_items, get_items, add_item
from django.views.decorators.csrf import csrf_exempt

data_dict_get = {'above_cemetery_item_id': None, 'name__icontains': None}
data_dict_add = {'above_cemetery_item': None, 'name': None}


def add_or_change_cemetery_item(request, pk=None):
    dict_filter = {'above_cemetery_item': None}
    cemetery_item = None
    if pk:
        cemetery_item = get_object_or_404(CemeteryItem, pk=pk)
    CemeteryItemFormSet = modelformset_factory(
        CemeteryItem, form=CemeteryItemForm, extra=0, can_delete=True
    )
    if request.method == 'POST':
        cemetery_item_formset = CemeteryItemFormSet(
            data=request.POST,
            prefix="cemetery_item",
            form_kwargs={"request": request},
        )
    else:
        CemeteryItem_queryset_result = get_tree_items(cemetery_item, CemeteryItem, dict_filter)
        cemetery_item_formset = CemeteryItemFormSet(
            queryset=CemeteryItem_queryset_result,
            prefix="cemetery_item",
            form_kwargs={"request": request}
        )

    context = {
        "cemetery_item_formset": cemetery_item_formset}
    return render(request, "cemetery_item.html", context)


@csrf_exempt
def get_cemetery_items(request):
    return get_items(request, CemeteryItem, data_dict_get)


@csrf_exempt
def add_cemetery_item(request):
    return add_item(request, CemeteryItem, data_dict_add)
