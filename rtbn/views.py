from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Person, \
    AddressItem,  \
    CallingTeam, \
    CallingDirection, \
    MilitaryEnlistmentOffice, \
    Hospital, \
    Hospitalization, \
    WarOperation, \
    WarArchievement, \
    Camp, \
    LabourTeam, \
    Captivity, \
    BeingCamped, \
    CompulsoryWork, \
    InfirmaryCamp, \
    Burial, \
    Reburial, \
    NameDistortion, \
    PatronimicDistortion, \
    SurnameDistortion
from address.models import AddressItem
from war_unit.models import WarUnit

from django import forms
from django.core.paginator import Paginator
from django.forms import modelformset_factory, inlineformset_factory, formset_factory
from django.http import JsonResponse
from django.forms import formset_factory, modelform_factory
from django.views.decorators.csrf import csrf_exempt
from .forms import PersonModelForm, \
    NameDistortionForm, \
    SurnameDistortionForm, \
    PatronimicDistortionForm, \
    MilitaryEnlistmentOfficeForm, \
    CallingDirectionForm, \
    AddressItemForm, \
    WarArchievementForm, \
    HospitalizationForm, \
    CaptivityForm, \
    BeingCampedForm, \
    CompusoryWorkForm, \
    InfirmaryCampForm, \
    BurialForm, \
    ReburialForm

from common.functions import get_data_by_name, add_data_with_name, save_formset_with_person


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
    burial = None
    reburial = None

    if pk:
        person = get_object_or_404(Person, pk=pk)
    CallingDirectionFormset = modelformset_factory(
        CallingDirection, form=CallingDirectionForm, extra=0, can_delete=True)
    WarArchievementFormset = modelformset_factory(
        WarArchievement, form=WarArchievementForm, extra=0, can_delete=True)
    HospitalizationFormset = modelformset_factory(
        Hospitalization, form=HospitalizationForm, extra=0, can_delete=True)
    CaptivityFormset = modelformset_factory(
        Captivity, form=CaptivityForm, extra=0, can_delete=True)
    BeingCampedFormset = modelformset_factory(
        BeingCamped, form=BeingCampedForm, extra=0, can_delete=True)
    CompulsoryWorkFormset = modelformset_factory(
        CompulsoryWork, form=CompusoryWorkForm, extra=0, can_delete=True)
    InfirmaryCampFormset = modelformset_factory(
        InfirmaryCamp, form=InfirmaryCampForm, extra=0, can_delete=True)

    if request.method == 'POST':
        person_form = PersonModelForm(request, data=request.POST, instance=person)
        calling_direction_formset = CallingDirectionFormset(
            queryset = CallingDirection.objects.filter(person=person),
            data = request.POST,
            prefix= "calling_direction",
            form_kwargs={"request": request},
        )

        war_achievement_formset = WarArchievementFormset(
            queryset = WarArchievement.objects.filter(person=person),
            data = request.POST,
            prefix= "war_archievement",
            form_kwargs={"request": request},
        )

        hospitalization_formset = HospitalizationFormset(
            queryset=Hospitalization.objects.filter(person=person),
            data = request.POST,
            prefix="hospitalization",
            form_kwargs={"request": request}
        )

        captivity_formset = CaptivityFormset(
            queryset=Captivity.objects.filter(person=person),
            data = request.POST,
            prefix="captivity",
            form_kwargs={"request": request}
        )

        being_camped_formset = BeingCampedFormset(
            queryset=BeingCamped.objects.filter(person=person),
            data = request.POST,
            prefix="being_camped",
            form_kwargs={"request": request}
        )

        compulsory_work_formset = CompulsoryWorkFormset(
            queryset=CompulsoryWork.objects.filter(person=person),
            data = request.POST,
            prefix="compulsory_work",
            form_kwargs={"request": request}
        )

        infirmary_camp_formset = InfirmaryCampFormset(
            queryset=CompulsoryWork.objects.filter(person=person),
            data = request.POST,
            prefix="infirmary_camp",
            form_kwargs={"request": request}
        )

        burial_form = BurialForm(request.POST)
        reburial_form = ReburialForm(request.POST) 

        if person_form.is_valid() \
            and calling_direction_formset.is_valid() \
            and war_achievement_formset.is_valid() \
            and hospitalization_formset.is_valid() \
            and captivity_formset.is_valid() \
            and being_camped_formset.is_valid() \
            and compulsory_work_formset.is_valid() \
            and infirmary_camp_formset.is_valid() \
            and burial_form.is_valid() \
            and reburial_form.is_valid():
            person = person_form.save()
            burial =  burial_form.save(commit=False)
            reburial = reburial_form.save(commit=False)
            burial.person = person
            reburial.person = person
            burial.save()
            burial.save()

            save_formset_with_person(calling_direction_formset, person)
            save_formset_with_person(war_achievement_formset, person)
            save_formset_with_person(hospitalization_formset, person)
            save_formset_with_person(captivity_formset, person)
            save_formset_with_person(being_camped_formset, person)
            save_formset_with_person(compulsory_work_formset, person)
            save_formset_with_person(infirmary_camp_formset, person)
            return redirect("person_detail", pk = person.pk)

    else:
        # forms
        person_form = PersonModelForm(request, instance=person)
        burial = Burial.objects.filter(person=person).first()
        reburial = Reburial.objects.filter(person=person).first()
        burial_form = BurialForm(request, instance=burial)
        reburial_form = ReburialForm(request, instance=reburial) 
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

        war_achievement_formset = WarArchievementFormset(
            queryset=WarArchievement.objects.filter(person=person),
            prefix="war_archievement",
            form_kwargs={"request": request}
        )

        hospitalization_formset = HospitalizationFormset(
            queryset=Hospitalization.objects.filter(person=person),
            prefix="hospitalization",
            form_kwargs={"request": request}
        )

        captivity_formset = CaptivityFormset(
            queryset=Captivity.objects.filter(person=person),
            prefix="captivity",
            form_kwargs={"request": request}
        )

        being_camped_formset = BeingCampedFormset(
            queryset=BeingCamped.objects.filter(person=person),
            prefix="being_camped",
            form_kwargs={"request": request}
        )

        compulsory_work_formset = CompulsoryWorkFormset(
            queryset=CompulsoryWork.objects.filter(person=person),
            prefix="compulsory_work",
            form_kwargs={"request": request}
        )

        infirmary_camp_formset = InfirmaryCampFormset(
            queryset=CompulsoryWork.objects.filter(person=person),
            prefix="infirmary_camp",
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
            'war_achievement_formset': war_achievement_formset,
            'hospitalization_formset': hospitalization_formset,
            'captivity_formset': captivity_formset,
            'being_camped_formset': being_camped_formset,
            'compulsory_work_formset': compulsory_work_formset,
            'infirmary_camp_formset': infirmary_camp_formset,
            'burial_form': burial_form,
            'reburial_form': reburial_form,
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

class PersonDetail(DetailView):
    model = Person
    context_object_name = "person"

def searching(request):
    return render(request, 'search.html')


def searching_param(request, type_search):
    return render(request, 'search.html', {'type_search': type_search})


@csrf_exempt
def region(request):
    if request.is_ajax():
        term = request.POST.get('term')
        parent_id = request.POST.get('parent_id')
        print('term is %s' % term)
        print('parent_id is %s' % parent_id)
        if term is not None:
            regions = AddressItem.objects.all().filter(
                name__icontains=term, parent_address_unit_id=parent_id)
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
            parent_address_unit=parent_region, name=d['text'])
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


@csrf_exempt
def calling_team(request):
    return get_data_by_name(request, CallingTeam)


@csrf_exempt
def add_calling_team(request):
    return add_data_with_name(request, CallingTeam)


@csrf_exempt
def war_operation(request):
    return get_data_by_name(request, WarOperation)


@csrf_exempt
def add_war_operation(request):
    return add_data_with_name(request, WarOperation)


@csrf_exempt
def hospital(request):
    return get_data_by_name(request, Hospital)


@csrf_exempt
def add_hospital(request):
    return add_data_with_name(request, Hospital)


@csrf_exempt
def camp(request):
    return get_data_by_name(request, Camp)


@csrf_exempt
def add_camp(request):
    return add_data_with_name(request, Camp)


@csrf_exempt
def labour_team(request):
    return get_data_by_name(request, LabourTeam)


@csrf_exempt
def add_labour_team(request):
    return add_data_with_name(request, LabourTeam)


def test(request):
    print('test')
    return HttpResponse("test")
