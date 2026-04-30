# stock/admin.py
from django.contrib import admin
from .models import Stock


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'warehouse',
        'product',
        'quantity',
    )

    search_fields = (
        'warehouse__name',
        'product__name',
        'product__barcode',
    )

    list_filter = ('warehouse',)