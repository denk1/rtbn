from django import forms
from .models import Person, AddressItem


class PersonModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        field = self.fields['name_distortion']
        field.required = False
        print(1)

    class Meta:
        model = Person
        fields = (
            'name',
            'name_distortion',
            'surname',
            'surname_distortion',
            'patronimic',
            'patronimic_distortion',
            'birthday')

        widgets = {
            "name": forms.TextInput(attrs={
                'placeholder': 'Имя',
                'class': 'form-control form-element',
                'name': 'name'}),
            "name_distortion": forms.TextInput(attrs={
                'placeholder': 'Возможное искажение',
                'class': 'form-control form-element',
                'name': 'name_distortion'}),
            "surname": forms.TextInput(attrs={
                'placeholder': 'Фамилия',
                'class': 'form-control form-element',
                'name': 'surname'}),
            "surname_distortion": forms.TextInput(attrs={
                'placeholder': 'Возможное искажение',
                'class': 'form-control form-element',
                'name': 'surname_distortion'}),
            "patronimic": forms.TextInput(attrs={
                'placeholder': 'Отчество',
                'class': 'form-control form-element',
                'name': 'patronimic'}),
            "patronimic_distortion": forms.TextInput(attrs={
                'placeholder': 'Возможное искажение',
                'class': 'form-control form-element',
                'name': 'patronimic_distortion'}),
            "birthday": forms.TextInput(attrs={
                'placeholder': 'Дата рождения',
                'class': 'form-control floating-label form-element',
                'name': 'birthday',
                'id': 'date_birthday'}),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = AddressItem
        fields = ('address_item_name',)
