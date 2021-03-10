from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Person, \
    WarUnitType, \
    AddressItem,  \
    WarUnit, \
    CallingTeam, \
    MilitaryEnlistmentOffice, \
    Call, \
    Hospital, \
    Hospitalization, \
    WarOperation, \
    WarArchievement, \
    Camp, \
    ArbeitCamp, \
    InfirmaryCamp, \
    Captivity, \
    Burial, \
    Reburial

from django.core.paginator import Paginator
from django.forms import modelformset_factory, inlineformset_factory, formset_factory
from django.http import JsonResponse
from django.forms import formset_factory
from django.views.decorators.csrf import csrf_exempt
from .forms import PersonModelForm, RegionBornForm, DistrictBornForm, LocalityBornForm


def index(request):
    persons = Person.objects.all()[:5]
    return render(request, 'index.html', {'persons_update': persons})


@login_required
def data_input(request):
    person_form = PersonModelForm(initial={"name": None})
    region_form = RegionBornForm()
    district_form = DistrictBornForm()
    locality_form = LocalityBornForm()
    context = {'person_form': person_form,
               'region_form': region_form,
               'district_form': district_form,
               'locality_form': locality_form}
    return render(request, 'data_input.html', context)


def persons_listing(request):
    persons_list = Person.objects.all()
    paginator = Paginator(persons_list, 25)
    page = request.GET.get('page')
    persons = paginator.get_page(page)
    if request.method == 'POST':
        FormsetPerson = modelformset_factory(Person, fields="__all__")
        FormsetAddressItem = modelformset_factory(
            AddressItem, fields="__all__")
        FormsetWarUnit = modelformset_factory(WarUnit, fields="__all__")
        FormsetWarServe = modelformset_factory(WarServe, fields="__all__")
        FormsetCallingTeam = modelformset_factory(
            CallingTeam, fields="__all__")
        FormsetCallingTeamDirection = modelformset_factory(
            CallingTeamDirection, fields="__all__")
        FormsetMilitaryEnlistmentOffice = modelformset_factory(
            MilitaryEnlistmentOffice, fields="__all__")
        FormsetMobilization = modelformset_factory(
            Mobilization, fields="__all__")
        FormsetCall = modelformset_factory(Call, fields="__all__")
        FormsetHospital = modelformset_factory(Hospital, fields="__all__")
        FormsetHospitalization = modelformset_factory(
            Hospitalization, fields="__all__")
        FormsetWarOperation = modelformset_factory(
            WarOperation, fields="__all__")
        FormsetWarArchievement = modelformset_factory(
            WarArchievement, fields="__all__")
        FormsetCamp = modelformset_factory(Camp, fields="__all__")
        FormsetCampArbeit = modelformset_factory(
            CampArbeit, fields="__all__")
        FormsetInfirmaryCamp = modelformset_factory(
            InfirmaryCamp, fields="__all__")
        FormsetCaptivity = modelformset_factory(Captivity, fields="__all__")
        FormsetBureal = modelformset_factory(Burial, fields="__all__")
        FormsetReburial = modelformset_factory(Reburial, fields="__all__")

        formset_person = FormsetPerson(request.POST, prefix="person")
        formset_warunit = FormsetWarUnit(request.POST, prefix="warunit")
        formset_warserve = FormsetWarServe(request.POST, prefix="warserve")
        formset_calling_team = FormsetCallingTeam(
            request.POST, prefix="calling_team")
        formset_calling_team_direction = FormsetCallingTeamDirection(
            request.POST, prefix="calling_team_direction")
        formset_enlistment_office = FormsetMilitaryEnlistmentOffice(
            request.POST, prefix="military_enlistment_office")
        formset_mobilization = FormsetMobilization(
            request.POST, prefix="mobilization")
        formset_call = FormsetCall(request.POST, prefix="call")
        formset_hospital = FormsetHospital(request.POST, prefix="hospital")
        formset_hospitalization = FormsetHospitalization(
            request.POST, prefix="hospitalization")
        formset_waroperation = FormsetWarOperation(
            request.POST, "waroperation")
        formset_war_archievement = FormsetWarArchievement(
            request.POST, "wararchievement")
        formset_camp = FormsetCamp(request.POST, prefix="camp")
        formset_camp_arbeit = FormsetCampArbeit(
            request.POST, prefix="camp_arbeit")
        formset_infirmary_camp = FormsetCampArbeit(
            request.POST, prefix="infirmary_camp")
        formset_captivity = FormsetCaptivity(request.POST, prefix="captivity")
        formset_bureal = FormsetBureal(request.POST, prefix="bureal")
        formset_rebureal = FormsetBureal(request.POST, prefix="rebureal")

    return render(request, 'persons_list.html', {'persons': persons})


def searching(requiest):
    return render(requiest, 'search.html')


def searching_param(requiest, type_search):
    return render(requiest, 'search.html', {'type_search': type_search})


@csrf_exempt
def region(request):

    if request.is_ajax():
        term = request.POST.get('term')
        type_item = request.POST.get('type_item')
        parent_id = request.POST.get('parent_id')
        print('parent_id is %s' % parent_id)
        if term is not None:
            regions = AddressItem.objects.all().filter(
                address_item_name__icontains=term, address_item_type=type_item, parent_address_unit_id=parent_id)
            response_content = list(regions.values())
            return JsonResponse(response_content, safe=False)


@csrf_exempt
def add_region(request):
    id = -1
    id_parent = None
    if request.method == 'POST':
        d = request.POST.dict()
        if "" != d['parent_item']:
            id_parent = d['parent_item']
        parent_region = AddressItem.objects.all().filter(id=id_parent).first()
        region = AddressItem.objects.create(
            parent_address_unit=parent_region, address_item_name=d['text'], address_item_type=TypePlace(int(d['type_item'])))
        region.save()
        id = region.id
        print(id)
        print(type(id))
    return JsonResponse({'result': True, 'id': id}, safe=False)
