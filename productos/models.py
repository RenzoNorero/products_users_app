from django.db import models
from .utils import random_number
from django.utils import timezone


# We define Class to storage products in the database
class Producto(models.Model):
    sku = models.AutoField(primary_key=True, default=random_number)
    name = models.CharField(max_length=50, null=True)
    brand = models.CharField(max_length=30, null=True)
    price = models.FloatField()
    click_count = models.PositiveIntegerField(default=0) # For counting clicks in each product
    

    def __str__(self):
        return self.name
