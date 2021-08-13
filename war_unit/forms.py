from django.forms import ModelForm
from .models import WarUnit


class WarUnitForm(ModelForm):
    class Meta:
        model = WarUnit
        fields = ('above_war_unit',)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)