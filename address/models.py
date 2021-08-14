from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
# Create your models here.


class AddressItem(MPTTModel):
    """
    address  
    """
    id = models.AutoField(primary_key=True)
    parent_address_unit = TreeForeignKey(
        'self', on_delete=models.CASCADE,
        null=True, blank=True,
        related_name='main_place')
    address_item_name = models.CharField(max_length=60)
    objects = models.Manager()

    def __str__(self):
        return self.address_item_name

    @property
    def name(self):
        return self.name

    class MPTTMeta:
        order_insertion_by = ['address_item_name']
        parent_attr = 'parent_address_unit'
