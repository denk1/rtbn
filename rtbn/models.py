from django_enumfield import enum
from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from address.models import AddressItem
from war_unit.models import WarUnit




class CallingTeam(models.Model):
    """
    Призывная команда
    """
    name = models.CharField(max_length=30, null=True)


class CallingDirection(models.Model):
    calling_team = models.ForeignKey(CallingTeam, on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    war_unit = models.ForeignKey(WarUnit, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['calling_team', 'person'], name='unique_team'),
            models.UniqueConstraint(
                fields=['person', 'war_unit'], name='unique_direction'),
        ]


class MilitaryEnlistmentOffice(models.Model):
    """
    Военкомат
    """
    id = models.AutoField(primary_key=True)
    address = models.ForeignKey(AddressItem, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Hospital(models.Model):
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

    def __str__(self):
        return self.name


class WarArchievement(models.Model):
    war_operation = models.ForeignKey(WarOperation, on_delete=models.CASCADE)
    war_unit = models.ForeignKey(WarUnit, on_delete=models.CASCADE)
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    period_from = models.DateField(null=False)
    period_to = models.DateField(null=False)


class Person(models.Model):
    """
    ФИО, дата рождения, мобилизация, последнее сообщение
    """
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    patronimic = models.CharField(max_length=30, null=True)
    birthday = models.DateField(null=True)
    born_locality = models.ForeignKey(
        AddressItem, related_name='born', on_delete=models.CASCADE, null=True)
    live_locality = models.ForeignKey(
        AddressItem, related_name='live', on_delete=models.CASCADE, null=True)
    military_enlistment_office = models.ForeignKey(
        MilitaryEnlistmentOffice, on_delete=models.CASCADE)
    mobilization = models.DateField()
    last_msg_locality = models.ForeignKey(
        AddressItem, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name + ' ' + self.surname + ' ' + self.father_name


class Camp(models.Model):
    """
    Лагерь
    """
    name = models.CharField(max_length=60)
    number = models.CharField(null=True, max_length=60)


class ArbeitCamp(models.Model):
    period_from = models.DateField(null=True)
    period_to = models.DateField(null=True)
    captivity = models.ForeignKey('Captivity', on_delete=models.CASCADE)
    name = models.CharField(max_length=60)


class InfirmaryCamp(models.Model):
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


class NameDistortion(models.Model):
    id = models.AutoField(primary_key=True)
    persons = models.ManyToManyField(Person)
    name = models.CharField(max_length=60)


class SurnameDistortion(models.Model):
    id = models.AutoField(primary_key=True)
    persons = models.ManyToManyField(Person)
    name = models.CharField(max_length=60)


class PatronimicDistortion(models.Model):
    id = models.AutoField(primary_key=True)
    persons = models.ManyToManyField(Person)
    name = models.CharField(max_length=60)
