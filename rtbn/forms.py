from django import forms
from crispy_forms import bootstrap, helper, layout
from .models import Person, \
    AddressItem, \
    NameDistortion, \
    SurnameDistortion, \
    PatronimicDistortion, \
    MilitaryEnlistmentOffice, \
    CallingTeam, \
    CallingDirection
from war_unit.models import WarUnit


class PersonModelForm(forms.ModelForm):
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
        bithday_field = layout.Field(
            "bithday", css_class="input-block-level")
        born_locality_field = layout.Field(
            "born_locality", css_class="input-block-level d-none test-class")
        live_locality_field = layout.Field(
            "live_locality", css_class="input-block-level d-none")
        mobilization_field = layout.Field(
            "mobilization", css_class="input-block-level")
        military_enlistment_office_field = layout.Field(
            "military_enlistment_office", css_class="input-block-level")

        last_msg_locality_field = layout.Field(
            "last_msg_locality", css_class="input-block-level")

        self.helper = helper.FormHelper()
        self.helper.form_tag = False
        self.helper.disable_csrf = True
        self.helper.layout = layout.Layout(
            name_field,
            surname_field,
            patronimic_filed,
            bithday_field,
            born_locality_field,
            mobilization_field,
            military_enlistment_office_field,
            last_msg_locality_field,
        )


class RegionBornForm(forms.ModelForm):
    FIELD_NAME_MAPPING = {
        'address_item_name': 'born_region_name',
    }

    def add_prefix(self, field_name):
        # look up field name; return original if not found
        field_name = self.FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(RegionBornForm, self).add_prefix(field_name)

    class Meta:
        model = AddressItem
        fields = ('address_item_name',)
        widgets = {
            'address_item_name': forms.Select(attrs={'id': 'born_region_name',
                                                     'name': 'born_region_name',
                                                     'style': 'width:200px',
                                                     'class': 'form-control form-element'}, choices=[('', 'Регион')]
                                              )
        }


class DistrictBornForm(forms.ModelForm):
    FIELD_NAME_MAPPING = {
        'address_item_name': 'born_district_name',
    }

    def add_prefix(self, field_name):
        # look up field name; return original if not found
        field_name = self.FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(DistrictBornForm, self).add_prefix(field_name)

    class Meta:
        model = AddressItem
        fields = ('address_item_name',)
        widgets = {
            'address_item_name': forms.Select(attrs={'id': 'born_district_name',
                                                     'name': 'born_district_name',
                                                     'style': 'width:200px',
                                                     'class': 'form-control form-element'}, choices=[('', 'Область')])
        }


class LocalityBornForm(forms.ModelForm):
    FIELD_NAME_MAPPING = {
        'address_item_name': 'born_locality_name',
    }

    def add_prefix(self, field_name):
        # look up field name; return original if not found
        field_name = self.FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(LocalityBornForm, self).add_prefix(field_name)

    class Meta:
        model = AddressItem
        fields = ('address_item_name',)
        widgets = {
            'address_item_name': forms.Select(attrs={'id': 'born_locality_name',
                                                     'name': 'born_locality_name',
                                                     'style': 'width:200px',
                                                     'class': 'form-control form-element'}, choices=[('', 'Район')])
        }


class RegionLiveForm(forms.ModelForm):
    FIELD_NAME_MAPPING = {
        'address_item_name': 'live_region_name',
    }

    def add_prefix(self, field_name):
        # look up field name; return original if not found
        field_name = self.FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(RegionLiveForm, self).add_prefix(field_name)

    class Meta:
        model = AddressItem
        fields = ('address_item_name',)
        widgets = {
            'address_item_name': forms.Select(attrs={'id': 'live_region_name',
                                                     'name': 'live_region_name',
                                                     'style': 'width:200px',
                                                     'class': 'form-control form-element'}, choices=[('', 'Регион')]
                                              )
        }


class DistrictLiveForm(forms.ModelForm):
    FIELD_NAME_MAPPING = {
        'address_item_name': 'live_district_name',
    }

    def add_prefix(self, field_name):
        # look up field name; return original if not found
        field_name = self.FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(DistrictLiveForm, self).add_prefix(field_name)

    class Meta:
        model = AddressItem
        fields = ('address_item_name',)
        widgets = {
            'address_item_name': forms.Select(attrs={'id': 'live_district_name',
                                                     'name': 'live_district_name',
                                                     'style': 'width:200px',
                                                     'class': 'form-control form-element'}, choices=[('', 'Область')])
        }


class LocalityLiveForm(forms.ModelForm):
    FIELD_NAME_MAPPING = {
        'address_item_name': 'live_locality_name',
    }

    def add_prefix(self, field_name):
        # look up field name; return original if not found
        field_name = self.FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(LocalityLiveForm, self).add_prefix(field_name)

    class Meta:
        model = AddressItem
        fields = ('address_item_name',)
        widgets = {
            'address_item_name': forms.Select(attrs={'id': 'live_locality_name',
                                                     'name': 'live_locality_name',
                                                     'style': 'width:200px',
                                                     'class': 'form-control form-element'}, choices=[('', 'Район')])
        }


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

# mobilization


class RegionWarEnlistmentForm(forms.ModelForm):
    FIELD_NAME_MAPPING = {
        'address_item_name': 'region_military_enlistment_office',
    }

    def add_prefix(self, field_name):
        # look up field name; return original if not found
        field_name = self.FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(RegionWarEnlistmentForm, self).add_prefix(field_name)

    class Meta:
        model = AddressItem
        fields = ('address_item_name',)
        widgets = {
            'address_item_name': forms.Select(attrs={'id': 'region_military_enlistment_office',
                                                     'name': 'region_military_enlistment_office',
                                                     'style': 'width:100px',
                                                     'class': 'form-control form-element'}, choices=[('', 'Область')])
        }


class DistrictWarEnlistmentForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    class Meta:
        model = AddressItem
        fields = ('address_item_name',)
        widgets = {
            'address_item_name': forms.Select(attrs={'id': 'district_military_enlistment_office',
                                                     'name': 'district_military_enlistment_office',
                                                     'style': 'width:100px',
                                                     'class': 'form-control form-element'}, choices=[('', 'Район')])
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


class RegionLetterForm(forms.ModelForm):

    FIELD_NAME_MAPPING = {
        'address_item_name': 'letter_region_name',
    }

    def add_prefix(self, field_name):
        # look up field name; return original if not found
        field_name = self.FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(RegionLetterForm, self).add_prefix(field_name)

    class Meta:
        model = AddressItem
        fields = ('address_item_name',)
        widgets = {
            'address_item_name': forms.Select(attrs={'id': 'letter_region_name',
                                                     'name': 'letter_region_name',
                                                     'style': 'width:200px',
                                                     'class': 'form-control form-element'}, choices=[('', 'Регион')]
                                              )
        }


class DistrictLetterForm(forms.ModelForm):
    FIELD_NAME_MAPPING = {
        'address_item_name': 'letter_district_name',
    }

    def add_prefix(self, field_name):
        # look up field name; return original if not found
        field_name = self.FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(DistrictLetterForm, self).add_prefix(field_name)

    class Meta:
        model = AddressItem
        fields = ('address_item_name',)
        widgets = {
            'address_item_name': forms.Select(attrs={'id': 'letter_district_name',
                                                     'name': 'letter_district_name',
                                                     'style': 'width:200px',
                                                     'class': 'form-control form-element'}, choices=[('', 'Область')])
        }


class LocalityLetterForm(forms.ModelForm):
    FIELD_NAME_MAPPING = {
        'address_item_name': 'letter_locality_name',
    }

    def add_prefix(self, field_name):
        # look up field name; return original if not found
        field_name = self.FIELD_NAME_MAPPING.get(field_name, field_name)
        return super(LocalityLetterForm, self).add_prefix(field_name)

    class Meta:
        model = AddressItem
        fields = ('address_item_name',)
        widgets = {
            'address_item_name': forms.Select(attrs={'id': 'letter_locality_name',
                                                     'name': 'letter_locality_name',
                                                     'style': 'width:200px',
                                                     'class': 'form-control form-element'}, choices=[('', 'Район')])
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
        exclude = ['programmer']

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
        id_field = layout.Field("id")

        calling_team_field = layout.Field(
            "calling_team", css_class="input-block-level")
    
        
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
