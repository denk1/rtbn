from django.forms import ModelForm
from .models import CemeteryItem


class CemeteryItemForm(ModelForm):
    class Meta:
        model = CemeteryItem
        fields = ('above_cemetery_item',)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)