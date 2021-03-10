from django.contrib import admin
from rtbn.models import Person, \
    MilitaryEnlistmentOffice, \
    AddressItem, \
    CallingTeam, \
    WarUnit, \
    Call, \
    Hospital, \
    Hospitalization, \
    WarOperation, \
    WarArchievement, \
    AddingInfo


admin.site.register(AddressItem)
admin.site.register(CallingTeam)
admin.site.register(MilitaryEnlistmentOffice)
admin.site.register(Person)
admin.site.register(WarUnit)
admin.site.register(Call)
admin.site.register(Hospital)
admin.site.register(Hospitalization)
admin.site.register(WarOperation)
admin.site.register(WarArchievement)
admin.site.register(AddingInfo)
