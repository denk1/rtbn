from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from .models import AddressItem
from .forms import AddressItemForm
from django.forms import modelformset_factory
from django.db.models import Q


def add_or_change_address(request, pk=None):
    address = None
    if pk:
        address = get_object_or_404(AddressItem, pk=pk)
    AddressItemFormSet = modelformset_factory(
        AddressItem, form=AddressItemForm, extra=0, can_delete=True
    )
    if request.method == 'POST':
        address_formset = AddressItemFormSet(
            data=request.POST,
            prefix="address",
            form_kwargs={"request": request},
        )
    else:
        address_queryset_result = AddressItem.objects.none()
        if address != None:
            address_queryset = AddressItem.objects.filter(pk=address.id)

            address_queryset_result |= address_queryset
            if len(address_queryset) != 0 and address_queryset[0].parent_address_unit is not None:
                while address_queryset:
                    above_address = AddressItem.objects.filter(
                        Q(pk=address_queryset[0].parent_address_unit.id)).exclude(parent_address_unit=None)
                    address_queryset_result |= above_address
                    address_queryset = above_address

        address_formset = AddressItemFormSet(
            queryset=address_queryset_result,
            prefix="address",
            form_kwargs={"request": request}
        )

    context = {
        "address_formset": address_formset}
    return render(request, "address.html", context)
