# movements/models.py
from django.db import models
from django.contrib.auth import get_user_model
from product.models import Product
from warehouse.models import Warehouse

User = get_user_model()


class Movement(models.Model):
    TYPE_CHOICES = (
        ('income', 'Kirim'),
        ('outcome', 'Chiqim'),
        ('transfer', 'Transfer'),
    )

    movement_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    from_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='from_moves'
    )

    to_warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='to_moves'
    )

    quantity = models.IntegerField()

    worker = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product.name