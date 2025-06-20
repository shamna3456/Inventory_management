from django.db import models

# Create your models here.

class ItemMaster(models.Model):
    item_name=models.CharField(max_length=50)
    description=models.TextField(max_length=300)
    has_expiry=models.BooleanField(default=False)
    has_entry_number=models.BooleanField(default=False)

class GoodsIn(models.Model):
    item=models.ForeignKey(ItemMaster,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    expiry_date=models.DateField(null=True)
    entry_number=models.IntegerField(null=True)
    date=models.DateTimeField(auto_now_add=True)

class GoodsOut(models.Model):
    item=models.ForeignKey(ItemMaster,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    date_removed=models.DateTimeField(auto_now_add=True)
