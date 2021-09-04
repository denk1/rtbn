from django.contrib import admin
from rtbn.models import Person, \
    MilitaryEnlistmentOffice, \
    AddressItem, \
    CallingTeam, \
    Hospital, \
    Hospitalization, \
    WarOperation, \
    WarArchievement

from mptt.admin import MPTTModelAdmin
from address.models import AddressItem
from war_unit.models import WarUnit


admin.site.register(AddressItem, MPTTModelAdmin)
admin.site.register(WarUnit, MPTTModelAdmin)
admin.site.register(CallingTeam)
admin.site.register(MilitaryEnlistmentOffice)
admin.site.register(Person)
admin.site.register(Hospital)
admin.site.register(Hospitalization)
admin.site.register(WarOperation)
admin.site.register(WarArchievement)
