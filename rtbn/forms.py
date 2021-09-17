from django import forms
from crispy_forms import bootstrap, helper, layout
from .models import Person, \
    AddressItem, \
    NameDistortion, \
    SurnameDistortion, \
    PatronimicDistortion, \
    MilitaryEnlistmentOffice, \
    CallingTeam, \
    CallingDirection, \
    WarArchievement, \
    Hospitalization, \
    Captivity, \
    BeingCamped, \
    CompulsoryWork, \
    InfirmaryCamp, \
    Burial, \
    Reburial
from war_unit.models import WarUnit
from .settings import DATE_INPUT_FORMATS


class PersonModelForm(forms.ModelForm):
    birthday = forms.DateField(input_formats=DATE_INPUT_FORMATS, required=False)
    mobilization = forms.DateField(input_formats=DATE_INPUT_FORMATS, required=False)

    class Meta:
        model = Person
        fields = ('__all__')

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        name_field = layout.Field(
            "name", css_class="input-block-level test")
        surname_field = layout.Field(
            "surname", css_class="input-block-level")
        patronimic_filed = layout.Field(
            "patronimic", css_class="input-block-level")
        birthday_field = layout.Field(
            "birthday", css_class="input-block-level date", input_formats=DATE_INPUT_FORMATS)
        born_locality_field = layout.Field(
            "born_locality", css_class="input-block-level d-none test-class")
        live_locality_field = layout.Field(
            "live_locality", css_class="input-block-level d-none")
        mobilization_field = layout.Field(
            "mobilization", css_class="input-block-level")
        military_enlistment_office_field = layout.Field(
            "military_enlistment_office", css_class="input-block-level")

        last_msg_locality_field = layout.Field(
            "last_msg_locality", css_class="input-block-level d-none")

        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = layout.Layout(
            name_field,
            surname_field,
            patronimic_filed,
            birthday_field,
            born_locality_field,
            mobilization_field,
            military_enlistment_office_field,
            last_msg_locality_field,
        )


class NameDistortionForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False

    class Meta:
        model = NameDistortion
        fields = ('name',)
        widgets = {"name": forms.Select(attrs={
            'placeholder': 'Возможное искажение',
            'class': 'form-control form-element',
            'name': 'name_distortion',
            'id': 'name_distortion'})}


class SurnameDistortionForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False

    class Meta:
        model = SurnameDistortion
        fields = ('name',)
        widgets = {'name': forms.Select(attrs={
            'placeholder': 'Возможное искажение',
            'class': 'form-control form-element',
            'name': 'surname_distortion',
            'id': 'surname_distortion'})}


class PatronimicDistortionForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False

    class Meta:
        model = PatronimicDistortion
        fields = ('name',)
        widgets = {
            'name': forms.Select(attrs={
                'placeholder': 'Возможное искажение',
                'class': 'form-control form-element',
                'name': 'patronimic_distortion',
                'id': 'patronimic_distortion'}),
        }


class MilitaryEnlistmentOfficeForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    class Meta:
        model = MilitaryEnlistmentOffice
        fields = ('address',)
        widgets = {
            'address': forms.Select(attrs={
                'placeholder': 'Название призывного пункта',
                'class': 'form-control form-element',
                'name': 'military_enlistment_office',
                'id': 'enlistment_office_address'}),
        }


class CallingTeamForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)

    class Meta:
        model = CallingTeam
        fields = ('name',)
        widgets = {
            'name': forms.Select(attrs={
                'placeholder': 'Призывная команда',
                'class': 'form-control form-element',
                'name': 'calling_team_name',
                'id': 'calling_team_name'}),
        }


class AddressItemForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    class Meta:
        model = AddressItem
        fields = ('parent_address_unit',)
        widgets = {
            'parent_address_unit': forms.Select(attrs={
                'style': 'width:200px',
                'class': 'form-control form-element'})
        }


class CallingDirectionForm(forms.ModelForm):

    class Meta:
        model = CallingDirection
        exclude = ["person"]

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        id_field = layout.Field("id")

        calling_team_field = layout.Field(
            "calling_team", css_class="input-block-level calling-team")

        war_unit_field = layout.Field(
            "war_unit", css_class="input-block-level invoke-modal hidden-select")

        war_unit_button = layout.ButtonHolder(layout.Button('war_unit_button',
                                                            'Подразделение',
                                                            css_class="input-block-level btn-unit invoke-modal"))

        delete_field = layout.Field(
            "DELETE", css_class="input-block-level")

        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = layout.Layout(
            id_field,
            calling_team_field,
            # begin_modal_field,
            war_unit_field,
            # end_modal_field,
            # war_unit_button,
            delete_field,
        )


class WarArchievementForm(forms.ModelForm):
    period_from = forms.DateField(input_formats=DATE_INPUT_FORMATS, required=False)
    period_to = forms.DateField(input_formats=DATE_INPUT_FORMATS, required=False)

    class Meta:
        model = WarArchievement
        exclude = ['person']

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        id_field = layout.Field("id")

        war_operation_field = layout.Field(
            "war_operation", css_class="input-block-level war-operation"
        )

        war_unit_field = layout.Field(
            "war_unit", css_class="input-block-level invoke-modal hidden-select"
        )

        war_unit_button = layout.ButtonHolder(layout.Button('war_unit_achievement_button',
                                                            'Подразделение',
                                                            css_class="input-block-level btn-unit invoke-modal"))

        period_from_field = layout.Field(
            "period_from", css_class="input-block-level date"
        )

        period_to_field = layout.Field(
            "period_to", css_class="input-block-level date"
        )

        delete_field = layout.Field(
            "DELETE", css_class="input-block-level")

        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = layout.Layout(
            id_field,
            war_operation_field,
            war_unit_field,
            period_from_field,
            period_to_field,
            delete_field,
        )


class HospitalizationForm(forms.ModelForm):
    period_from = forms.DateField(input_formats=DATE_INPUT_FORMATS, required=False)
    period_to = forms.DateField(input_formats=DATE_INPUT_FORMATS, required=False)

    class Meta:
        model = Hospitalization
        exclude = ['person']

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        id_field = layout.Field("id")

        hospital_field = layout.Field(
            "hospital", css_class="input-block-level hospital"
        )

        hospital_location_field = layout.Field(
            "hospital_location", css_class="input-block-level test-class d-none hidden-select-address"
        )

        period_from_field = layout.Field(
            "period_from", css_class="input-block-level date"
        )

        period_to_field = layout.Field(
            "period_to", css_class="input-block-level date"
        )

        war_unit_consist_field = layout.Field(
            "war_unit_consist", css_class="input-block-level invoke-modal hidden-select"
        )

        war_unit_direction_field = layout.Field(
            "war_unit_direction", css_class="input-block-level invoke-modal hidden-select"
        )

        delete_field = layout.Field(
            "DELETE", css_class="input-block-level")

        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = layout.Layout(
            id_field,
            hospital_field,
            hospital_location_field,
            period_from_field,
            period_to_field,
            war_unit_consist_field,
            war_unit_direction_field,
            delete_field,
        )


class CaptivityForm(forms.ModelForm):
    date_of_captivity = forms.DateField(input_formats=DATE_INPUT_FORMATS, required=False)

    class Meta:
        model = Captivity
        exclude = ['person']

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        id_field = layout.Field("id")

        date_of_captivity_field = layout.Field(
            "date_of_captivity", css_class="input-block-level date"
        )

        place_of_captivity_field = layout.Field(
            "place_of_captivity", css_class="input-block-level date d-none hidden-select-address"
        )

        delete_field = layout.Field(
            "DELETE", css_class="input-block-level")

        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = layout.Layout(
            id_field,
            date_of_captivity_field,
            place_of_captivity_field,
            delete_field
        )


class BeingCampedForm(forms.ModelForm):
    period_from = forms.DateField(input_formats=DATE_INPUT_FORMATS, required=False)
    period_to = forms.DateField(input_formats=DATE_INPUT_FORMATS, required=False)

    class Meta:
        model = BeingCamped
        exclude = ['person']

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        id_field = layout.Field("id")

        period_from_field = layout.Field(
            "period_from", css_class="input-block-level date"
        )

        period_to_field = layout.Field(
            "period_to", css_class="input-block-level date"
        )

        camp_field = layout.Field(
            "camp", css_class="input-block-level camp"
        )

        number_field = layout.Field(
            "number", css_class="input-block-level test"
        )

        delete_field = layout.Field(
            "DELETE", css_class="input-block-level")

        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = layout.Layout(
            id_field,
            period_from_field,
            period_to_field,
            camp_field,
            number_field,
            delete_field
        )


class CompusoryWorkForm(forms.ModelForm):
    period_from = forms.DateField(input_formats=DATE_INPUT_FORMATS, required=False)
    period_to = forms.DateField(input_formats=DATE_INPUT_FORMATS, required=False)

    class Meta:
        model = CompulsoryWork
        exclude = ['person']

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        id_field = layout.Field("id")

        period_from_field = layout.Field(
            "period_from", css_class="input-block-level date"
        )

        period_to_field = layout.Field(
            "period_to", css_class="input-block-level date"
        )

        labour_team_field = layout.Field(
            "labour_team", css_class="input-block-level labour-team"
        )

        delete_field = layout.Field(
            "DELETE", css_class="input-block-level")

        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = layout.Layout(
            id_field,
            period_from_field,
            period_to_field,
            labour_team_field,
            delete_field
        )


class InfirmaryCampForm(forms.ModelForm):
    period_from = forms.DateField(input_formats=DATE_INPUT_FORMATS, required=False)
    period_to = forms.DateField(input_formats=DATE_INPUT_FORMATS, required=False)

    class Meta:
        model = InfirmaryCamp
        exclude = ['person']

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        id_field = layout.Field("id")

        period_from_field = layout.Field(
            "period_from", css_class="input-block-level date"
        )

        period_to_field = layout.Field(
            "period_to", css_class="input-block-level date"
        )

        camp_field = layout.Field(
            "camp", css_class="input-block-level camp"
        )

        delete_field = layout.Field(
            "DELETE", css_class="input-block-level")

        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = layout.Layout(
            id_field,
            period_from_field,
            period_to_field,
            camp_field,
            delete_field
        )


class BurialForm(forms.ModelForm):
    date_of_burial = forms.DateField(input_formats=DATE_INPUT_FORMATS,  required=False)

    class Meta:
        model = Burial
        exclude = ['person']

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        date_of_burial_field = layout.Field(
            "date_of_burial", css_class="input-block-level date"
        )

        address_doc_field = layout.Field(
            "address_doc", css_class="input-block-level hidden-select-address"
        )

        address_act_field = layout.Field(
            "address_act", css_class="input-block-level hidden-select-address"
        )

        cemetery_item_field = layout.Field(
            "cemetery_item", css_class="input-block-level hidden-select-cemetery"
        )

        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = layout.Layout(
            date_of_burial_field,
            address_doc_field,
            address_act_field,
            cemetery_item_field
        )


class ReburialForm(forms.ModelForm):
    date_of_reburial = forms.DateField(input_formats=DATE_INPUT_FORMATS, required=False)

    class Meta:
        model = Reburial
        exclude = ['person']

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        date_of_reburial_field = layout.Field(
            "date_of_reburial", css_class="input-block-level date")

        reburial_cause_field = layout.Field(
            "reburial_cause", css_class="input-block-level"
        )

        address_field = layout.Field(
            "address", css_class="input-block-level hidden-select-address"
        )

        cemetery_item_field = layout.Field(
            "cemetery_item", css_class="input-block-level hidden-select-cemetery"
        )

        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = layout.Layout(
            date_of_reburial_field,
            reburial_cause_field,
            address_field,
            cemetery_item_field
        )
