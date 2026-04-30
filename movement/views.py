# dashboard/views.py
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from product.models import Product
from warehouse.models import Warehouse
from remaing.models import Stock
from movement.models import Movement
from django.shortcuts import get_object_or_404

def scan_page(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'scan.html', {
        'warehouses': warehouses
    })


def scan_submit(request):
    if request.method == 'POST':
        barcode = request.POST.get('barcode')
        qty_str = request.POST.get('quantity')
        action = request.POST.get('action')
        warehouse_id = request.POST.get('warehouse')

        # Bo'sh maydonlarni tekshirish
        if not barcode or not warehouse_id or not qty_str:
            messages.error(request, "Barcha maydonlarni to'ldiring!")
            return redirect('scan_page')

        qty = int(qty_str)

        try:
            product = Product.objects.get(barcode=barcode)
            warehouse = Warehouse.objects.get(id=warehouse_id)
        except Product.DoesNotExist:
            messages.error(request, "Mahsulot topilmadi")
            return redirect('scan_page')
        except Warehouse.DoesNotExist:
            messages.error(request, "Ombor topilmadi")
            return redirect('scan_page')

        stock, created = Stock.objects.get_or_create(
            product=product,
            warehouse=warehouse,
            defaults={'quantity': 0} # Agar yangi stock bo'lsa 0 dan boshlasin
        )

        if action == 'income':
            stock.quantity += qty
            Movement.objects.create(
                movement_type='income',
                product=product,
                to_warehouse=warehouse,
                quantity=qty,
                worker=request.user
            )
            messages.success(request, f"{product.name} - {qty} ta kirim qilindi.")

        elif action == 'outcome':
            if stock.quantity < qty:
                messages.error(request, f"Omborda yetarli qoldiq yo'q! (Mavjud: {stock.quantity})")
                return redirect('scan_page')

            stock.quantity -= qty
            Movement.objects.create(
                movement_type='outcome',
                product=product,
                from_warehouse=warehouse,
                quantity=qty,
                worker=request.user
            )
            messages.success(request, f"{product.name} - {qty} ta chiqim qilindi.")

        stock.save()
        return redirect('scan_page')





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