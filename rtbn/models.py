from django_enumfield import enum
from django.conf import settings
from mptt.models import MPTTModel, TreeForeignKey
from django.db import models
from django.urls import reverse
from address.models import AddressItem
from war_unit.models import WarUnit
from cemetery.models import CemeteryItem
from core.models import CreationModificationDateBase, UrlBase


class CallingTeam(models.Model):
    name = models.CharField("Название призывной команды",
                            max_length=30, null=True)

    def __str__(self):
        return self.name


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
    id = models.AutoField(primary_key=True)
    address = models.ForeignKey(AddressItem, on_delete=models.CASCADE)
    name = models.CharField("Название военкомата", max_length=50)

    def __str__(self):
        return self.name


class Hospital(models.Model):
    name = models.CharField("Название госпиталя", max_length=256)

    def __str__(self):
        return self.name


class Hospitalization(models.Model):
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE)
    hospital_location = models.ForeignKey(
        AddressItem, on_delete=models.CASCADE, null=True)
    period_from = models.DateField("C:", null=False)
    period_to = models.DateField("По:", null=False)
    war_unit_consist = models.ForeignKey(
        WarUnit, on_delete=models.CASCADE, related_name='consist')
    war_unit_direction = models.ForeignKey(
        WarUnit, on_delete=models.CASCADE, null=True, related_name='direction')


class WarOperation(models.Model):
    name = models.CharField("Название военной операции", max_length=256)

    def __str__(self):
        return self.name


class WarArchievement(models.Model):
    war_operation = models.ForeignKey(WarOperation, on_delete=models.CASCADE)
    war_unit = models.ForeignKey(WarUnit, on_delete=models.CASCADE)
    person = models.ForeignKey("Person", on_delete=models.CASCADE)
    period_from = models.DateField(null=False)
    period_to = models.DateField(null=False)


class Person(CreationModificationDateBase, UrlBase):
    name = models.CharField("Имя", max_length=30)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Пользователь",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="written_by_user",
    )
    surname = models.CharField("Фамилия", max_length=30)
    patronimic = models.CharField("Отчество", max_length=30, null=True)
    birthday = models.DateField("Дата рождения", null=True)
    born_locality = models.ForeignKey(
        AddressItem, related_name='born', on_delete=models.CASCADE, null=True)
    live_locality = models.ForeignKey(
        AddressItem, related_name='live', on_delete=models.CASCADE, null=True)
    military_enlistment_office = models.ForeignKey(
        MilitaryEnlistmentOffice, on_delete=models.CASCADE)
    mobilization = models.DateField("Дата мобилизации")
    last_msg_locality = models.ForeignKey(
        AddressItem, on_delete=models.CASCADE, null=True)
    is_defector = models.BooleanField("Перебесчик")
    is_gestapo = models.BooleanField("Гестапо")
    is_frei = models.BooleanField("Освобождён")

    def __str__(self):
        return self.name + ' ' + self.surname + ' ' + self.patronimic
        
    def get_url_path(self):
        return reverse("person_details", kwargs={
            "person_id": str(self.pk),
        })


class Camp(models.Model):
    name = models.CharField("Название лагеря", max_length=60)

    def __str__(self):
        return self.name


class LabourTeam(models.Model):
    name = models.CharField("Название рабочий команды", max_length=60)

    def __str__(self):
        return self.name


class Captivity(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    date_of_captivity = models.DateField("Дата попадания в плен", null=True)
    place_of_captivity = models.ForeignKey(
        AddressItem, null=True, on_delete=models.CASCADE)


class BeingCamped(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    period_from = models.DateField(null=True)
    period_to = models.DateField(null=True)
    camp = models.ForeignKey(Camp, on_delete=models.CASCADE, null=True)
    number = models.CharField("Номер военнопленного", max_length=60)


class CompulsoryWork(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    period_from = models.DateField(null=True)
    period_to = models.DateField(null=True)
    labour_team = models.ForeignKey(
        LabourTeam, on_delete=models.CASCADE, null=True)


class InfirmaryCamp(models.Model):
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    period_from = models.DateField(null=True)
    period_to = models.DateField(null=True)
    camp = models.ForeignKey(Camp, on_delete=models.CASCADE, null=True)


class Burial(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    date_of_burial = models.DateField(null=True)
    address_doc = models.ForeignKey(
        AddressItem, on_delete=models.CASCADE, related_name='address_item_doc_id')
    address_act = models.ForeignKey(
        AddressItem, on_delete=models.CASCADE, related_name='address_item_act_id')
    cemetery_item = models.ForeignKey(
        CemeteryItem, on_delete=models.CASCADE)


class Reburial(models.Model):
    person = models.OneToOneField(Person, on_delete=models.CASCADE)
    date_of_reburial = models.DateField(null=True)
    reburial_cause = models.CharField(max_length=80, null=True)
    address = models.ForeignKey(AddressItem, on_delete=models.CASCADE)
    cemetery_item = models.ForeignKey(
        CemeteryItem, on_delete=models.CASCADE)


class NameDistortion(models.Model):
    id = models.AutoField(primary_key=True)
    persons = models.ManyToManyField(Person)
    name = models.CharField("Искажение имени", max_length=60)


class SurnameDistortion(models.Model):
    id = models.AutoField(primary_key=True)
    persons = models.ManyToManyField(Person)
    name = models.CharField("Икажение фамилии", max_length=60)


class PatronimicDistortion(models.Model):
    id = models.AutoField(primary_key=True)
    persons = models.ManyToManyField(Person)
    name = models.CharField("Искажения в отчестве", max_length=60)
