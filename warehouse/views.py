# dashboard/views.py

from django.shortcuts import render
from django.db.models import Sum, Count
from product.models import Product
from warehouse.models import Warehouse
from remaing.models import Stock


def dashboard(request):
    # cards
    total_products = Product.objects.count()
    total_warehouses = Warehouse.objects.count()

    total_stock = Stock.objects.aggregate(
        total=Sum('quantity')
    )['total'] or 0

    main_warehouses = Warehouse.objects.filter(
        warehouse_type='main'
    ).count()

    branch_warehouses = Warehouse.objects.filter(
        warehouse_type='branch'
    ).count()

    # recent products
    recent_products = Product.objects.order_by('-id')[:8]

    # warehouse stock
    warehouse_stock = Stock.objects.values(
        'warehouse__name'
    ).annotate(
        total_qty=Sum('quantity'),
        total_products=Count('product')
    ).order_by('-total_qty')

    # low stock
    low_stock = Stock.objects.select_related(
        'product',
        'warehouse'
    ).filter(quantity__lte=5)[:10]

    context = {
        'total_products': total_products,
        'total_warehouses': total_warehouses,
        'total_stock': total_stock,
        'main_warehouses': main_warehouses,
        'branch_warehouses': branch_warehouses,
        'recent_products': recent_products,
        'warehouse_stock': warehouse_stock,
        'low_stock': low_stock,
    }

    return render(request, 'base.html', context)