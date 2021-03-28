from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Person, \
    TypePlace, \
    WarUnitType, \
    AddressItem,  \
    WarUnit, \
    CallingTeam, \
    CallingDirection, \
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
    Reburial, \
    NameDistortion, \
    PatronimicDistortion, \
    SurnameDistortion

from django import forms
from django.core.paginator import Paginator
from django.forms import modelformset_factory, inlineformset_factory, formset_factory
from django.http import JsonResponse
from django.forms import formset_factory, modelform_factory
from django.views.decorators.csrf import csrf_exempt
from .forms import PersonModelForm, \
    RegionLiveForm, \
    DistrictLiveForm, \
    LocalityLiveForm, \
    RegionBornForm, \
    DistrictBornForm, \
    LocalityBornForm, \
    NameDistortionForm, \
    SurnameDistortionForm, \
    PatronimicDistortionForm, \
    CallForm, \
    RegionWarEnlistmentForm, \
    DistrictWarEnlistmentForm, \
    MilitaryEnlistmentOfficeForm, \
    RegionLetterForm, \
    DistrictLetterForm, \
    LocalityLetterForm


def index(request):
    persons = Person.objects.all()[:5]
    return render(request, 'index.html', {'persons_update': persons})


@login_required
def data_input(request):
    person_form = PersonModelForm(initial={"name": None, "surname": None})
    region_born_form = RegionBornForm(initial={'address_item_name': 'Регион'}, prefix="region_region")
    district_born_form = DistrictBornForm(prefix="prefix_district")
    locality_born_form = LocalityBornForm(prefix="prefix_locality")
    region_live_form = RegionLiveForm(initial={'address_item_name': 'Регион'})
    district_live_form = DistrictLiveForm()
    locality_live_form = LocalityLiveForm()
    name_distortion_form = NameDistortionForm()
    surname_distortion_form = SurnameDistortionForm()
    patronimic_distortion_form = PatronimicDistortionForm()
    # moblization
    call_form = CallForm()
    region_war_enlistment_form = RegionWarEnlistmentForm()
    district_war_enlistment_form = DistrictWarEnlistmentForm()
    military_enlistment_office_form = MilitaryEnlistmentOfficeForm()
    region_letter_form = RegionLetterForm()
    district_letter_form = DistrictLetterForm()
    locality_letter_form = LocalityLetterForm()
    calling_team_form = modelform_factory(CallingDirection,
        fields=('calling_team', 'war_unit',),
        widgets={
            'calling_team': forms.Select(attrs={
                                                     'style': 'width:200px',
                                                     'class': 'form-control form-element'}),
            'war_unit': forms.Select(attrs={
                                                     'style': 'width:200px',
                                                     'class': 'form-control form-element'})

            }
    )

    context = {
               'person_form': person_form,
               'region_born_form': region_born_form,
               'district_born_form': district_born_form,
               'locality_born_form': locality_born_form,
               'region_live_form': region_live_form,
               'district_live_form': district_live_form,
               'locality_live_form': locality_live_form,
               'name_distortion_form': name_distortion_form,
               'surname_distortion_form': surname_distortion_form,
               'patronimic_distortion_form': patronimic_distortion_form,
               'call_form': call_form,
               'region_war_enlistment_form': region_war_enlistment_form,
               'district_war_enlistment_form': district_war_enlistment_form,
               'military_enlistment_office_form': military_enlistment_office_form,
               'region_letter_form': region_letter_form,
               'district_letter_form': district_letter_form,
               'locality_letter_form': locality_letter_form,
               'calling_team_form': calling_team_form
               }

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
        FormsetCallingTeam = modelformset_factory(
            CallingTeam, fields="__all__")
        FormsetMilitaryEnlistmentOffice = modelformset_factory(
            MilitaryEnlistmentOffice, fields="__all__")
        FormsetCall = modelformset_factory(Call, fields="__all__")
        FormsetHospital = modelformset_factory(Hospital, fields="__all__")
        FormsetHospitalization = modelformset_factory(
            Hospitalization, fields="__all__")
        FormsetWarOperation = modelformset_factory(
            WarOperation, fields="__all__")
        FormsetWarArchievement = modelformset_factory(
            WarArchievement, fields="__all__")
        FormsetCamp = modelformset_factory(Camp, fields="__all__")
        FormsetInfirmaryCamp = modelformset_factory(
            InfirmaryCamp, fields="__all__")
        FormsetCaptivity = modelformset_factory(Captivity, fields="__all__")
        FormsetBureal = modelformset_factory(Burial, fields="__all__")
        FormsetReburial = modelformset_factory(Reburial, fields="__all__")

        formset_person = FormsetPerson(request.POST, prefix="person")
        formset_warunit = FormsetWarUnit(request.POST, prefix="warunit")
        formset_calling_team = FormsetCallingTeam(
            request.POST, prefix="calling_team")
        formset_enlistment_office = FormsetMilitaryEnlistmentOffice(
            request.POST, prefix="military_enlistment_office")
        formset_call = FormsetCall(request.POST, prefix="call")
        formset_hospital = FormsetHospital(request.POST, prefix="hospital")
        formset_hospitalization = FormsetHospitalization(
            request.POST, prefix="hospitalization")
        formset_waroperation = FormsetWarOperation(
            request.POST, "waroperation")
        formset_war_archievement = FormsetWarArchievement(
            request.POST, "wararchievement")
        formset_camp = FormsetCamp(request.POST, prefix="camp")
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


@csrf_exempt
def distortion(request):
    if request.is_ajax():
        term = request.POST.get('term')
        type_item = int(request.POST.get('type_item'))
        print(term, type_item)
        distortions = None
        if type_item == 0:
            if term is not None:
                distortions = NameDistortion.objects.all().filter(
                    name__icontains=term)
        elif type_item == 1:
            if term is not None:
                distortions = PatronimicDistortion.objects.all().filter(
                    name__icontains=term)
        else:
            if term is not None:
                distortions = SurnameDistortion.objects.all().filter(
                    name__icontains=term)
        response_content = list(distortions.values())
        return JsonResponse(response_content, safe=False)


@csrf_exempt
def add_distortion(request):
    id = -1
    id_parent = None
    if request.method == 'POST':
        d = request.POST.dict()
        distortion = None
        if int(d['type_item']) == 0:
            distortion = NameDistortion.objects.create(
                name=d['text'])
        elif int(d['type_item']) == 1:
            distortion = PatronimicDistortion.objects.create(
                name=d['text'])
        else:
            distortion = SurnameDistortion.objects.create(
                name=d['text'])
        distortion.save()
        id = distortion.id
        print(id)
        print(type(id))
    return JsonResponse({'result': True, 'id': id}, safe=False)
