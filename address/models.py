from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from core.models import TreeItemAbstruct
# Create your models here.


class AddressItem(MPTTModel, TreeItemAbstruct):
    """
    address  
    """
    id = models.AutoField(primary_key=True)
    parent_address_unit = TreeForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='main_place')
    name = models.CharField(max_length=60)
    objects = models.Manager()

    def __str__(self):
        return self.name

    @property
    def get_parent(self):
        return self.parent_address_unit

    @property
    def get_full_str(self):
        dict_filter = {'parent_address_unit': None}
        return self.get_tree(self, type(self), dict_filter) + ' ' + self.name

    class MPTTMeta:
        order_insertion_by = ['name']
        parent_attr = 'parent_address_unit'
