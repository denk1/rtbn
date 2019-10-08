from enumfields import EnumField
from enumfields import Enum
from django.db import models

class TypePlace(Enum):
    """
    тип адресной компоненты
    """
    LOCALITY = 1
    DISTRICT = 2
    REGION = 3
    REPUBLIC = 4


class WarUnitType(Enum):
    FRONT = 1
    ARMY = 2
    DIVISION = 3
    RGT = 4
    COY = 5
    UNIT = 6


class AddressItem(models.Model):
    """
    Адрес 
    """
    above_address_unit = models.ForeignKey("AddressItem", null=True, on_delete=models.CASCADE)
    address_item_name = models.CharField(max_length=60)
    address_item_type = EnumField(TypePlace, max_length=1)


class WarUnit(models.Model):
    """
    Подразделения
    """
    above_war_init = models.ForeignKey("WarUnit", null=True, on_delete=models.CASCADE)
    military_personnel = models.ManyToManyField("Person", through='WarServe')
    name = models.CharField(max_length=60)
    warunit_type = EnumField(WarUnitType, max_length=1)


class WarServe(models.Model):
    """
    Военная служба
    """
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    war_unit = models.ForeignKey(WarUnit, on_delete=models.CASCADE)
    

class CallingTeam(models.Model):
    """
    Призывная команда
    """
    name = models.CharField(max_length=30, null=True)


class CallingTeamDirection(models.Model):
    calling_team = models.ForeignKey(CallingTeam, on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)


class MilitaryEnlistmentOffice(models.Model):
    """
    Военкомат
    """
    address = models.ForeignKey(AddressItem, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)


class Mobilization(models.Model):
    date_mobilization = models.DateField()


class Call(models.Model):
    military_enlistment_office = models.ForeignKey(MilitaryEnlistmentOffice, on_delete=models.CASCADE)
    mobilization = models.ForeignKey(Mobilization, on_delete=models.CASCADE)
    warunit = models.ForeignKey(WarUnit, on_delete=models.CASCADE)
    last_msg_locality = models.ForeignKey(AddressItem, on_delete=models)


class Hospital(models.Model):
    patients = models.ManyToManyField("Person", through='Hospitalization')
    name = models.CharField(max_length=256)


class Hospitalization(models.Model):
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    hospital= models.ForeignKey(Hospital, on_delete=models.CASCADE)
    period_from = models.DateField(null=False)
    period_to = models.DateField(null=False)
    war_unit_consist = models.ForeignKey(WarUnit, on_delete=models.CASCADE)
    direction_name = models.CharField(max_length=256)


class WarOperation(models.Model):
    name = models.CharField(max_length=256)
    participants = models.ManyToManyField(WarServe, through="WarArchievement")
    def __str__(self):
        return self.name


class WarArchievement(models.Model):
    war_operation = models.ForeignKey(WarOperation, on_delete=models.CASCADE)
    war_serve = models.ForeignKey(WarServe, on_delete=models.CASCADE)
    period_from = models.DateField(null=False)
    period_to = models.DateField(null=False)
    

class Person(models.Model):
    """
    ФИО, дата рождения, мобилизация, последнее сообщение
    """
    name = models.CharField(max_length=30, default='Неизвестно')
    name_distortion = models.CharField(max_length=30, null=True)
    surname = models.CharField(max_length=30, default='Неизвестно')
    surname_distortion = models.CharField(max_length=30, null=True)
    father_name = models.CharField(max_length=30, null=True)
    father_name_distortion = models.CharField(max_length=30, null=True)
    birthday = models.DateField(null=True)
    born_locality = models.ForeignKey(AddressItem, related_name='born', on_delete=models.CASCADE)
    live_locality = models.ForeignKey(AddressItem, related_name='live', on_delete=models.CASCADE)
    calling_teams = models.ManyToManyField(CallingTeam, through="CallingTeamDirection")
    call = models.ForeignKey(Call, on_delete=models.CASCADE)
    def __str__(self):
        return self.name + ' ' + self.surname + ' ' + self.father_name


class Camp(models.Model):
    """
    Лагерь
    """
    name = models.CharField(max_length=60)
    number = models.CharField(null=True, max_length=60)
    prisoners = models.ManyToManyField(Person, through='Captivity')


class CampArbeit(models.Model):
    camp = models.ForeignKey(Camp, on_delete=models.CASCADE)
    period_from = models.DateField(null=True)
    period_to = models.DataFieild(null=True)
    captivity = models.ForeignKey('Captivity', on_delete=models.CASCADE)
    name = models.CharField(max_length=60)


class InfirmaryCamp(models.Model):
    camp = models.ForeignKey(Camp, on_delete=models.CASCADE)
    period_from = models.DateField(null=True)
    period_to = models.DateField(null=True)
    captivity = models.ForeignKey('Captivity', on_delete=models.CASCADE)
    name = models.CharField(max_length=60)


class Captivity(models.Model):
    """
    Плен
    """
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    camp = models.ForeignKey(Camp, on_delete=models.CASCADE)
    date_of_captivity = models.DateField(null=True)
    place_of_captivity = models.ForeignKey(AddressItem, null=True, on_delete=models.CASCADE)
    

class AddingInfo(models.Model):
    """
    Дополнительная информация
    """
    person = models.OneToOneField('Person', on_delete=models.CASCADE)
    is_defector = models.BooleanField()
    is_gestapo = models.BooleanField()
    is_frei = models.BooleanField()