from django.contrib import admin
from rtbn.models import Person, \
    MilitaryEnlistmentOffice, \
    AddressItem, \
    CallingTeam, \
    WarUnit, \
    Hospital, \
    Hospitalization, \
    WarOperation, \
    WarArchievement, \
    AddingInfo

from mptt.admin import MPTTModelAdmin
from address.models import AddressItem


admin.site.register(AddressItem, MPTTModelAdmin)
admin.site.register(CallingTeam)
admin.site.register(MilitaryEnlistmentOffice)
admin.site.register(Person)
admin.site.register(WarUnit)
admin.site.register(Hospital)
admin.site.register(Hospitalization)
admin.site.register(WarOperation)
admin.site.register(WarArchievement)
admin.site.register(AddingInfo)
