from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import WarUnit
from .forms import WarUnitForm
from django.forms import modelformset_factory
from common.functions import get_tree_items, get_items, add_item
from django.views.decorators.csrf import csrf_exempt

data_dict_get = {'above_war_unit_id': None, 'name__icontains': None}
data_dict_add = {'above_war_unit': None, 'name': None}


def add_or_change_warunit(request, pk=None):
    dict_filter = {'above_war_unit': None}
    war_unit = None
    if pk:
        war_unit = get_object_or_404(WarUnit, pk=pk)
    WarUnitFormSet = modelformset_factory(
        WarUnit, form=WarUnitForm, extra=0, can_delete=True
    )
    if request.method == 'POST':
        warunit_formset = WarUnitFormSet(
            data=request.POST,
            prefix="warunit",
            form_kwargs={"request": request},
        )
    else:
        warunit_queryset_result = get_tree_items(
            war_unit, WarUnit, dict_filter)
        warunit_formset = WarUnitFormSet(
            queryset=warunit_queryset_result,
            prefix="warunit",
            form_kwargs={"request": request}
        )

    context = {
        "warunit_formset": warunit_formset}
    return render(request, "war_unit.html", context)


@csrf_exempt
def get_war_units(request):
    return get_items(request, WarUnit, data_dict_get)


@csrf_exempt
def add_war_unit(request):
    return add_item(request, WarUnit, data_dict_add)


def get_full_str(request, pk=None):
    war_unit = get_object_or_404(WarUnit, pk=pk)
    return JsonResponse({'result': True, 'full_str': war_unit.get_full_str}, safe=False)
