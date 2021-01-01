from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Person, \
    WarUnitType, \
    AddressItem,  \
    WarUnit, \
    WarServe, \
    CallingTeam, \
    CallingTeamDirection, \
    MilitaryEnlistmentOffice, \
    Mobilization, \
    Call, \
    Hospital, \
    Hospitalization, \
    WarOperation, \
    WarArchievement, \
    Camp, \
    CampArbeit, \
    InfirmaryCamp, \
    Captivity, \
    Burial, \
    Reburial

from django.core.paginator import Paginator
from django.forms import modelformset_factory, inlineformset_factory, formset_factory


def index(request):
    persons = Person.objects.all()[:5]
    return render(request, 'index.html', {'persons_update': persons})


@login_required
def data_input(request):
    return render(request, 'data_input.html')


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
