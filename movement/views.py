# dashboard/views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from product.models import Product
from warehouse.models import Warehouse
from remaing.models import Stock
from movement.models import Movement


def scan_page(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'scan.html', {
        'warehouses': warehouses
    })


def scan_submit(request):
    if request.method == 'POST':
        barcode = request.POST.get('barcode')
        qty = int(request.POST.get('quantity'))
        action = request.POST.get('action')
        warehouse_id = request.POST.get('warehouse')

        try:
            product = Product.objects.get(barcode=barcode)
        except Product.DoesNotExist:
            messages.error(request, "Mahsulot topilmadi")
            return redirect('scan')

        warehouse = Warehouse.objects.get(id=warehouse_id)

        stock, created = Stock.objects.get_or_create(
            product=product,
            warehouse=warehouse
        )

        # 🔥 KIRIM
        if action == 'income':
            stock.quantity += qty

            Movement.objects.create(
                movement_type='income',
                product=product,
                to_warehouse=warehouse,
                quantity=qty,
                worker=request.user
            )

        # 🔥 CHIQIM
        elif action == 'outcome':
            if stock.quantity < qty:
                messages.error(request, "Yetarli mahsulot yo‘q")
                return redirect('scan')

            stock.quantity -= qty

            Movement.objects.create(
                movement_type='outcome',
                product=product,
                from_warehouse=warehouse,
                quantity=qty,
                worker=request.user
            )

        stock.save()

        messages.success(request, "Bajarildi ✅")
        return redirect('scan')





def get_product_by_barcode(request):
    barcode = request.GET.get('barcode')

    try:
        product = Product.objects.get(barcode=barcode)
        return JsonResponse({
            'success': True,
            'name': product.name
        })
    except Product.DoesNotExist:
        return JsonResponse({
            'success': False
        })