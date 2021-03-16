from django import forms
from .models import Person, \
    AddressItem, \
    NameDistortion, \
    SurnameDistortion, \
    PatronimicDistortion


class PersonModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Person
        fields = (
            'name',
            'surname',
            'patronimic',
            'birthday')

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
        }


class RegionBornForm(forms.ModelForm):
    class Meta:
        model = AddressItem
        fields = ('address_item_name',)
        widgets = {
            'address_item_name': forms.Select(attrs={'id': 'born_region_name',
                                                     'name': 'born_region_name',
                                                     'style': 'width:200px',
                                                     'class': 'mdb-select md-form'}, choices=[('', 'Регион')]
                                              )
        }


class DistrictBornForm(forms.ModelForm):
    class Meta:
        model = AddressItem
        fields = ('address_item_name',)
        widgets = {
            'address_item_name': forms.Select(attrs={'id': 'born_district_name',
                                                     'name': 'born_district_name',
                                                     'style': 'width:200px',
                                                     'class': 'mdb-select md-form'}, choices=[('', 'Область')])
        }


class LocalityBornForm(forms.ModelForm):
    class Meta:
        model = AddressItem
        fields = ('address_item_name',)
        widgets = {
            'address_item_name': forms.Select(attrs={'id': 'born_locality_name',
                                                     'name': 'born_locality_name',
                                                     'style': 'width:200px',
                                                     'class': 'mdb-select md-form'}, choices=[('', 'Район')])
        }


class RegionLiveForm(forms.ModelForm):
    class Meta:
        model = AddressItem
        fields = ('address_item_name',)
        widgets = {
            'address_item_name': forms.Select(attrs={'id': 'live_region_name',
                                                     'name': 'live_region_name',
                                                     'style': 'width:200px',
                                                     'class': 'mdb-select md-form'}, choices=[('', 'Регион')]
                                              )
        }


class DistrictLiveForm(forms.ModelForm):
    class Meta:
        model = AddressItem
        fields = ('address_item_name',)
        widgets = {
            'address_item_name': forms.Select(attrs={'id': 'live_district_name',
                                                     'name': 'live_district_name',
                                                     'style': 'width:200px',
                                                     'class': 'mdb-select md-form'}, choices=[('', 'Область')])
        }


class LocalityLiveForm(forms.ModelForm):
    class Meta:
        model = AddressItem
        fields = ('address_item_name',)
        widgets = {
            'address_item_name': forms.Select(attrs={'id': 'live_locality_name',
                                                     'name': 'live_locality_name',
                                                     'style': 'width:200px',
                                                     'class': 'mdb-select md-form'}, choices=[('', 'Район')])
        }


class NameDistortionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name_distortion'].required = False

    class Meta:
        model = NameDistortion
        fields = ('name_distortion',)
        widgets = {"name_distortion": forms.TextInput(attrs={
            'placeholder': 'Возможное искажение',
            'class': 'form-control form-element',
            'name': 'surname_distortion'})}


class SurnameDistortionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['surname_distortion'].required = False

    class Meta:
        model = SurnameDistortion
        fields = ('surname_distortion',)
        widgets = {"surname_distortion": forms.TextInput(attrs={
            'placeholder': 'Возможное искажение',
            'class': 'form-control form-element',
            'name': 'surname_distortion'})}


class PatronimicDistortionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['patronimic_distortion'].required = False

    class Meta:
        model = PatronimicDistortion
        fields = ('patronimic_distortion',)
        widgets = {
            "patronimic_distortion": forms.TextInput(attrs={
                'placeholder': 'Возможное искажение',
                'class': 'form-control form-element',
                'name': 'patronimic_distortion'}),
        }
