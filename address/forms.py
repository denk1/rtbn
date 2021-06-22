from django.forms import ModelForm
from .models import AddressItem


class AddressItemForm(ModelForm):
    class Meta:
        model = AddressItem
        fields = ('parent_address_unit',)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)
