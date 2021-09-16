from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from core.models import TreeItemAbstruct


class WarUnit(MPTTModel, TreeItemAbstruct):
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

    @property
    def get_full_str(self):
        dict_filter = {'above_war_unit': None}
        return self.get_tree(self, type(self), dict_filter) + ' ' + self.name

    class MPTTMeta:
        order_insertion_by = ['name']
        parent_attr = 'above_war_unit'
