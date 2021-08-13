from django.shortcuts import render, redirect, get_object_or_404
from .models import WarUnit
from .forms import WarUnitForm
from django.forms import modelformset_factory
from common.functions import get_tree_items, get_items, add_item
from django.views.decorators.csrf import csrf_exempt

data_dict = {'above_war_unit': None, 'unit_name' : None}

def add_or_change_warunit(request, pk=None):
    war_unit = None
    if pk:
        print("get_object_or_404")
        war_unit = get_object_or_404(WarUnit, pk=pk)
    WarUnitFormSet = modelformset_factory(
        WarUnit, form=WarUnitForm, extra=0, can_delete=True
    )
    if request.method == 'POST':
        war_unit_formset = WarUnitFormSet(
            data=request.POST,
            prefix="warunit",
            form_kwargs={"request": request},
        )
    else:
        warunit_queryset_result = get_tree_items(war_unit, WarUnit)
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
    return get_items(request, WarUnit, data_dict)

@csrf_exempt
def add_war_unit(request):
    return add_item(request, WarUnit, data_dict)

