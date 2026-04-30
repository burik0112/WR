# warehouse/admin.py
from django.contrib import admin
from .models import Warehouse


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'warehouse_type',
        'parent',
    )

    search_fields = ('name',)
    list_filter = ('warehouse_type',)