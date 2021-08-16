from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class WarUnit(MPTTModel):
    """
    war units
    """
    id = models.AutoField(primary_key=True)
    above_war_unit = TreeForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='main_unit')
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

    @property
    def get_parent(self):
        return self.above_war_unit

    class MPTTMeta:
        order_insertion_by = ['name']
        parent_attr = 'above_war_unit'
