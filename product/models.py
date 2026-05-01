# products/models.py
from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=100, unique=True)   # strix kod
    raw_barcode = models.TextField(null=True, blank=True)
    sku = models.CharField(max_length=100, blank=True, null=True)

    purchase_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name