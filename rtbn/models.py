from django_enumfield import enum
from mptt.models import MPTTModel, TreeForeignKey
from django.db import models


class TypePlace(enum.Enum):
    """
    тип адресной компоненты
    """
    LOCALITY = 1
    DISTRICT = 2
    REGION = 3
    REPUBLIC = 4


class WarUnitType(enum.Enum):
    FRONT = 1
    ARMY = 2
    DIVISION = 3
    RGT = 4
    COY = 5
    UNIT = 6


class AddressItem(MPTTModel):
    """
    Адрес 
    """
    id = models.AutoField(primary_key=True)
    parent_address_unit = TreeForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='main_place')
    address_item_name = models.CharField(max_length=60)
    address_item_type = enum.EnumField(TypePlace)
    objects = models.Manager()

    def __str__(self):
        return self.address_item_name

    class MPTTMeta:
        order_insertion_by = ['address_item_name']
        parent_attr = 'parent_address_unit'


class WarUnit(models.Model):
    """
    Подразделения
    """
    above_war_unit = models.ForeignKey(
        "WarUnit", null=True, on_delete=models.CASCADE)
    military_personnel = models.ManyToManyField("Person", through='WarServe')
    name = models.CharField(max_length=60)
    warunit_type = enum.EnumField(WarUnitType)


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
    military_enlistment_office = models.ForeignKey(
        MilitaryEnlistmentOffice, on_delete=models.CASCADE)
    mobilization = models.ForeignKey(Mobilization, on_delete=models.CASCADE)
    warunit = models.ForeignKey(WarUnit, on_delete=models.CASCADE, null=True)
    last_msg_locality = models.ForeignKey(
        AddressItem, on_delete=models.CASCADE, null=True)


class Hospital(models.Model):
    patients = models.ManyToManyField("Person", through='Hospitalization')
    name = models.CharField(max_length=256)


class Hospitalization(models.Model):
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    hospital_location = models.ForeignKey(
        AddressItem, on_delete=models.CASCADE, null=True)
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
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, default='Неизвестно')
    name_distortion = models.CharField(max_length=30, null=True)
    surname = models.CharField(max_length=30, default='Неизвестно')
    surname_distortion = models.CharField(max_length=30, null=True)
    patronimic = models.CharField(max_length=30, null=True)
    patronimic_distortion = models.CharField(max_length=30, null=True)
    birthday = models.DateField(null=True)
    born_locality = models.ForeignKey(
        AddressItem, related_name='born', on_delete=models.CASCADE, null=True)
    live_locality = models.ForeignKey(
        AddressItem, related_name='live', on_delete=models.CASCADE, null=True)
    calling_teams = models.ManyToManyField(
        CallingTeam, through="CallingTeamDirection")
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
    period_to = models.DateField(null=True)
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
    place_of_captivity = models.ForeignKey(
        AddressItem, null=True, on_delete=models.CASCADE)


class AddingInfo(models.Model):
    """
    Дополнительная информация
    """
    person = models.OneToOneField('Person', on_delete=models.CASCADE)
    is_defector = models.BooleanField()
    is_gestapo = models.BooleanField()
    is_frei = models.BooleanField()


class Burial(models.Model):
    """
    Захоронение
    """
    person = models.OneToOneField(
        Person, on_delete=models.CASCADE, primary_key=True)
    date_of_burial = models.DateField(null=True)
    number_plot = models.CharField(max_length=30)
    address_doc = models.ForeignKey(
        AddressItem, on_delete=models.CASCADE, related_name='address_item_doc_id')
    address_act = models.ForeignKey(
        AddressItem, on_delete=models.CASCADE, related_name='address_item_act_id')
    cemetery = models.CharField(max_length=60)
    number_plot = models.CharField(max_length=30)
    number_line = models.CharField(max_length=30)
    number_thumb = models.CharField(max_length=30)


class Reburial(models.Model):
    """
    Перезахоронение
    """
    burial = models.OneToOneField(
        Burial, on_delete=models.CASCADE, primary_key=True)
    date_of_reburial = models.DateField(null=True)
    reburial_cause = models.CharField(max_length=60, null=True)
    address = models.ForeignKey(AddressItem, on_delete=models.CASCADE)
