from django import forms
from .models import Person, \
    AddressItem, \
    NameDistortion, \
    SurnameDistortion, \
    PatronimicDistortion, \
    MilitaryEnlistmentOffice, \
    Call, \
    CallingTeam, \
    CallingDirection


class PersonModelForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    class Meta:
        model = Person
        fields = (
            'name',
            'surname',
            'patronimic',
            'birthday',
            'born_locality',
            'live_locality')

        widgets = {
            "name": forms.TextInput(attrs={
                'placeholder': 'Имя',
                'class': 'form-control form-element',
                'name': 'name'}),

            "surname": forms.TextInput(attrs={
                'placeholder': 'Фамилия',
                'class': 'form-control form-element',
                'name': 'surname'}),

            "patronimic": forms.TextInput(attrs={
                'placeholder': 'Отчество',
                'class': 'form-control form-element',
                'name': 'patronimic'}),

            "birthday": forms.TextInput(attrs={
                'placeholder': 'Дата рождения',
                'class': 'form-control floating-label form-element',
                'name': 'birthday',
                'id': 'date_birthday'}),
            'born_locality': forms.Select(attrs={
                'style': 'width:200px',
                'class': 'form-control form-element'}),
            'live_locality': forms.Select(attrs={
                'style': 'width:200px',
                'class': 'form-control form-element'})

        }


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


class CallForm(forms.ModelForm):
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args)

    class Meta:
        model = Call
        fields = ('mobilization', 'military_enlistment_office',
                  'last_msg_locality')
        widgets = {
            'mobilization': forms.TextInput(attrs={'id': 'date_mobilization', 'class': 'form-control form-element',
                                                   'placeholder': 'Дата мобилизации',
                                                   'name': 'date_mobilization'}),
            'military_enlistment_office': forms.Select(attrs={'id': 'military_enlistment_office', 'class': 'form-control form-element',
                                                              'placeholder': 'Военкомат',
                                                              'name': 'military_enlistment_office'}),
            'last_msg_locality': forms.Select(attrs={'id': 'last_msg_locality', 'class': 'form-control form-element',
                                                     'placeholder': 'Населенный пункт',
                                                     'name': 'last_msg_locality'})
        }


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
    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    class Meta:
        model = CallingDirection
        exclude = ('person',)
