# stock/models.py
from django.db import models
from product.models import Product
from warehouse.models import Warehouse


class Stock(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    quantity = models.IntegerField(default=0)

    class Meta:
        unique_together = ('warehouse', 'product')

    def __str__(self):
        return f"{self.warehouse.name} - {self.product.name}"