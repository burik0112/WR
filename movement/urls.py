# dashboard/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('scan/', views.scan_page, name='scan'),
    path('scan/submit/', views.scan_submit, name='scan_submit'),
    path('get-product/', views.get_product_by_barcode, name='get_product'),
]
