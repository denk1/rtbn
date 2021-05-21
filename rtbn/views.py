from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Person, \
    TypePlace, \
    WarUnitType, \
    AddressItem,  \
    WarUnit, \
    CallingTeam, \
    CallingDirection, \
    MilitaryEnlistmentOffice, \
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
    RegionWarEnlistmentForm, \
    DistrictWarEnlistmentForm, \
    MilitaryEnlistmentOfficeForm, \
    RegionLetterForm, \
    DistrictLetterForm, \
    LocalityLetterForm, \
    CallingDirectionForm, \
    AddressItemForm


def index(request):
    persons = Person.objects.all()[:5]
    return render(request, 'index.html', {'persons_update': persons})


@login_required
def data_input(request):
    person_form = PersonModelForm(initial={"name": None, "surname": None})
    name_distortion_form = NameDistortionForm()
    surname_distortion_form = SurnameDistortionForm()
    patronimic_distortion_form = PatronimicDistortionForm()
    # moblization
    call_form = CallForm()
    district_born_form = modelform_factory(
        AddressItem, fields=('parent_address_unit',), widgets={
            'parent_address_unit': forms.Select(attrs={
                'style': 'width:200px',
                'class': 'form-control form-element'})
        })
    district_born_form.prefix = 'born_region'
    locality_born_form = modelform_factory(
        AddressItem, fields=('parent_address_unit',), widgets={
            'parent_address_unit': forms.Select(attrs={
                'style': 'width:200px',
                'class': 'form-control form-element'})
        })
    locality_born_form.prefix = 'born_district'

    district_live_form = modelform_factory(
        AddressItem, fields=('parent_address_unit',), widgets={
            'parent_address_unit': forms.Select(attrs={
                'style': 'width:200px',
                'class': 'form-control form-element'})
        })
    district_live_form.prefix = 'live_region'
    locality_live_form = modelform_factory(
        AddressItem, fields=('parent_address_unit',), widgets={
            'parent_address_unit': forms.Select(attrs={
                'style': 'width:200px',
                'class': 'form-control form-element'})
        })
    locality_live_form.prefix = 'live_district'

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
    military_enlistment_office_form = modelform_factory(
        MilitaryEnlistmentOffice, fields=('address',),
        widgets={
            'address': forms.Select(attrs={
                'style': 'width:200px',
                'class': 'form-control form-element'})
        }
    )

    address_war_enlistment_form = modelform_factory(
        AddressItem, fields=('parent_address_unit',), widgets={
            'parent_address_unit': forms.Select(attrs={
                'style': 'width:200px',
                'class': 'form-control form-element'})
        }
    )
    address_war_enlistment_form.prefix = 'enlistment_region'

    district_letter_form = modelform_factory(
        AddressItem, fields=('parent_address_unit',), widgets={
            'parent_address_unit': forms.Select(attrs={
                'style': 'width:200px',
                'class': 'form-control form-element'})
        })
    district_letter_form.prefix = 'letter_region'
    locality_letter_form = modelform_factory(
        AddressItem, fields=('parent_address_unit',), widgets={
            'parent_address_unit': forms.Select(attrs={
                'style': 'width:200px',
                'class': 'form-control form-element'})
        })
    locality_letter_form.prefix = 'letter_district'

    context = {
        'person_form': person_form,
        'district_born_form': district_born_form,
        'locality_born_form': locality_born_form,
        'district_live_form': district_live_form,
        'locality_live_form': locality_live_form,
        'name_distortion_form': name_distortion_form,
        'surname_distortion_form': surname_distortion_form,
        'patronimic_distortion_form': patronimic_distortion_form,
        'call_form': call_form,
        'address_war_enlistment_form': address_war_enlistment_form,
        'military_enlistment_office_form': military_enlistment_office_form,
        'district_letter_form': district_letter_form,
        'locality_letter_form': locality_letter_form,
        'calling_team_form': calling_team_form
    }

    return render(request, 'person_form.html', context)


@login_required
def add_or_change_person(request, pk=None):
    person = None
    locality_born = None
    district_born = None
    region_born = None
    locality_live = None
    district_live = None
    region_live = None
    name_distortion = None
    surname_distortion = None
    patronimic_distortion = None
    call = None
    military_enlistment_office = None
    address_war_enlistment = None
    last_msg_locality = None
    calling_direction = None
    last_msg_locality = None
    last_msg_district = None

    if pk:
        person = get_object_or_404(Person, pk=pk)
    CallingDirectionFormset = modelformset_factory(
        CallingDirection, form=CallingDirectionForm, extra=0, can_delete=True)
    if request.method == 'POST':

        locality_born = AddressItem.objects.filter(id=person.born_locality)
        district_born = AddressItem.objects.filter(
            id=locality_born.parent_address_unit)
        region_born = AddressItem.objects.filter(
            id=district_born.parent_address_unit)
        locality_live = AddressItem.objects.filter(id=person.live_locality)
        district_live = AddressItem.objects.filter(
            id=locality_live.parent_address_unit)
        region_live = AddressItem.objects.filter(
            id=district_live.parent_address_unit)
        name_distortion = NameDistortion.objects.filter(persons=person)[0]
        surname_distortion = SurnameDistortion.objects.filter(persons=person)[
            0]
        patronimic_distortion = PatronimicDistortion.objects.filter(persons=person)[
            0]
        military_enlistment_office = MilitaryEnlistmentOffice.objects.filter(
            pk=call.military_enlistment_office)
        address_war_enlistment = AddressItem.objects.filter(
            pk=military_enlistment_office.address)
        last_msg_locality = AddressItem.objects.filter(
            pk=call.last_msg_locality)
        calling_direction = CallingDirection.objects.filter(person=person)
        last_msg_locality = AddressItem.objects.filter(
            pk=call.last_msg_locality)
        last_msg_district = AddressItem.objects.filter(
            pk=last_msg_locality.parent_address_unit)
    else:
        # forms
        person_form = PersonModelForm(request, instance=person)
        #person_form = PersonModelForm(initial={"name": None, "surname": None})
        name_distortion_form = NameDistortionForm(
            request, instance=name_distortion, prefix='name_dist')
        surname_distortion_form = SurnameDistortionForm(
            request, instance=surname_distortion, prefix='surname_dist')
        patronimic_distortion_form = PatronimicDistortionForm(
            request, instance=patronimic_distortion, prefix='patronimic_dist')

        military_enlistment_office_form = MilitaryEnlistmentOfficeForm(
            request, instance=military_enlistment_office)

        calling_direction_formset = CallingDirectionFormset(
            queryset=CallingDirection.objects.filter(person=person),
            prefix="calling_direction",
            form_kwargs={"request": request}
        )

        address_war_enlistment_form = AddressItemForm(
            request, instance=address_war_enlistment, prefix='enlistment_office'
        )

        locality_born_form = AddressItemForm(
            request, instance=locality_born, prefix="locality_born")
        district_born_form = AddressItemForm(
            request, instance=district_born, prefix="district_born")
        locality_live_form = AddressItemForm(
            request, instance=locality_live, prefix="locality_live")
        district_live_form = AddressItemForm(
            request, instance=district_live, prefix="district_live")
        locality_letter_form = AddressItemForm(
            request, instance=last_msg_locality, prefix="locality_lst")
        district_letter_form = AddressItemForm(
            request, instance=last_msg_district, prefix="district_lst")

        context = {
            'person_form': person_form,
            'district_born_form': district_born_form,
            'locality_born_form': locality_born_form,
            'district_live_form': district_live_form,
            'locality_live_form': locality_live_form,
            'name_distortion_form': name_distortion_form,
            'surname_distortion_form': surname_distortion_form,
            'patronimic_distortion_form': patronimic_distortion_form,
            'address_war_enlistment_form': address_war_enlistment_form,
            'military_enlistment_office_form': military_enlistment_office_form,
            'district_letter_form': district_letter_form,
            'locality_letter_form': locality_letter_form,
            'calling_direction_formset': calling_direction_formset,
        }

    return render(request, 'person_form.html', context)


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


@csrf_exempt
def enlistment_office(request):
    if request.is_ajax():
        term = request.POST.get('term')
        type_item = request.POST.get('type_item')
        parent_id = request.POST.get('parent_id')
        print('parent_id is %s' % parent_id)
        if term is not None:
            military_enlistment_office = MilitaryEnlistmentOffice.objects.all().filter(
                name__icontains=term, address=parent_id)
            response_content = list(military_enlistment_office.values())
            return JsonResponse(response_content, safe=False)


@csrf_exempt
def add_enlistment_office(request):
    id = -1
    id_parent = None
    if request.method == 'POST':
        d = request.POST.dict()
        if "" != d['parent_item']:
            id_parent = d['parent_item']
        parent_region = AddressItem.objects.all().filter(id=id_parent).first()
        military_enlistment_office = MilitaryEnlistmentOffice.objects.create(
            address=parent_region, name=d['text'])
        military_enlistment_office.save()
        id = military_enlistment_office.id
        print(id)
    return JsonResponse({'result': True, 'id': id}, safe=False)
