# products/admin.py
from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'barcode',
        'sku',
        'purchase_price',
        'sale_price',
        'created_at',
    )

    search_fields = ('name', 'barcode', 'sku')
    list_filter = ('created_at',)