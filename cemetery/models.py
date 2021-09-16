from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from core.models import TreeItemAbstruct


class CemeteryItem(MPTTModel, TreeItemAbstruct):
    id = models.AutoField(primary_key=True)
    above_cemetery_item = TreeForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='main_unit')
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

    @property
    def get_parent(self):
        return self.above_cemetery_item

    @property
    def get_full_str(self):
        dict_filter = {'above_cemetery_item': None}
        return self.get_tree(self, type(self), dict_filter) + ' ' + self.name

    class MPTTMeta:
        order_insertion_by = ['name']
        parent_attr = 'above_cemetery_item'
