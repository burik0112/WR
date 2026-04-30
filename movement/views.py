from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from product.models import Product
from warehouse.models import Warehouse
from remaing.models import Stock
from movement.models import Movement


@login_required  # Faqat login qilganlar skaner qila oladi
def scan_page(request):
    warehouses = Warehouse.objects.all()
    return render(request, 'scan.html', {
        'warehouses': warehouses
    })


def get_product_by_barcode(request):
    barcode = request.GET.get('barcode')
    print("SCAN:", barcode)

    try:
        product = Product.objects.get(barcode=barcode)
        print("FOUND:", product.name)

        return JsonResponse({
            'success': True,
            'name': product.name
        })
    except Product.DoesNotExist:
        print("NOT FOUND")

        return JsonResponse({
            'success': False
        })


@login_required
def scan_submit(request):
    if request.method == 'POST':
        barcode = request.POST.get('barcode')
        qty_str = request.POST.get('quantity')
        action = request.POST.get('action')
        warehouse_id = request.POST.get('warehouse')

        # 1. Ma'lumotlar to'liqligini tekshirish
        if not all([barcode, qty_str, action, warehouse_id]):
            messages.error(request, "Barcha maydonlarni to'ldiring!")
            return redirect('scan_page')

        qty = int(qty_str)

        try:
            product = Product.objects.get(barcode=barcode)
            warehouse = Warehouse.objects.get(id=warehouse_id)

            # Stockni olish yoki yaratish
            stock, created = Stock.objects.get_or_create(
                product=product,
                warehouse=warehouse,
                defaults={'quantity': 0}
            )

            if action == 'income':
                stock.quantity += qty
                Movement.objects.create(
                    movement_type='income',
                    product=product,
                    to_warehouse=warehouse,
                    quantity=qty,
                    worker=request.user  # Endi xato bermaydi
                )
                messages.success(request, f"{product.name} - {qty} ta kirim qilindi.")

            elif action == 'outcome':
                if stock.quantity < qty:
                    messages.error(request, f"Omborda yetarli emas! (Mavjud: {stock.quantity})")
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

        except Product.DoesNotExist:
            messages.error(request, "Mahsulot topilmadi!")
        except Exception as e:
            messages.error(request, f"Xatolik: {str(e)}")

        return redirect('scan')