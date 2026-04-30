# warehouse/models.py
from django.db import models


class Warehouse(models.Model):
    TYPE_CHOICES = (
        ('main', 'Main'),
        ('branch', 'Branch'),
    )

    name = models.CharField(max_length=255)
    warehouse_type = models.CharField(max_length=20, choices=TYPE_CHOICES)

    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name