# movements/admin.py
from django.contrib import admin
from .models import Movement


@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'movement_type',
        'product',
        'from_warehouse',
        'to_warehouse',
        'quantity',
        'worker',
        'created_at',
    )

    search_fields = (
        'product__name',
        'product__barcode',
        'worker__username',
    )

    list_filter = (
        'movement_type',
        'created_at',
    )

    date_hierarchy = 'created_at'