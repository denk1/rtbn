from django.contrib import admin
from rtbn.models import Person, \
                                               Mobilization, \
                                               MilitaryEnlistmentOffice, \
                                               Region, \
                                               District, \
                                               Locality, \
                                               CallingTeam, \
                                               WarUnit, \
                                               WarServe, \
                                               CallingTeamDirection, \
                                               Call, \
                                               Hospital, \
                                               Hospitalization, \
                                               WarOperation, \
                                               WarArchievement


admin.site.register(District)
admin.site.register(CallingTeam)
admin.site.register(Locality)
admin.site.register(Mobilization)
admin.site.register(MilitaryEnlistmentOffice)
admin.site.register(Person)
admin.site.register(Region)
admin.site.register(WarUnit)
admin.site.register(WarServe)
admin.site.register(CallingTeamDirection)
admin.site.register(Call)
admin.site.register(Hospital)
admin.site.register(Hospitalization)
admin.site.register(WarOperation)
admin.site.register(WarArchievement)