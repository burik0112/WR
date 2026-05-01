from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from product.models import Product


# Create your views here.

from django.shortcuts import render, redirect

def product_create(request):
    if request.method == "POST":
        # MA'LUMOTNI SAQLASH QISMI (POST)
        name = request.POST.get('name')
        barcode = request.POST.get('barcode')
        sku = request.POST.get('sku')
        purchase_price = request.POST.get('purchase_price')
        sale_price = request.POST.get('sale_price')

        if not barcode or not name:
            messages.error(request, "Shtrix-kod va mahsulot nomi bo'lishi shart!")
            return redirect('product_create')

        p_price = purchase_price if purchase_price and purchase_price.strip() else 0
        s_price = sale_price if sale_price and sale_price.strip() else 0

        product, created = Product.objects.get_or_create(
            barcode=barcode,
            defaults={
                'name': name,
                'sku': sku,
                'purchase_price': p_price,
                'sale_price': s_price,
            }
        )

        if created:
            messages.success(request, f"Yangi mahsulot saqlandi: {name}")
            return redirect('product_list') # Saqlagandan keyin ro'yxatga qaytadi
        else:
            messages.warning(request, "Bu mahsulot allaqachon bor!")
            return redirect('product_create')

    # SAHIFANI KO'RSATISH QISMI (GET) - HTML shu yerda ulanadi!
    # 'product_create.html' bu siz skaner kodi bor HTML faylingiz nomi
    return render(request, 'product_add.html')



def product_list(request):
    products = Product.objects.all().order_by('-id')

    return render(request, 'product_list.html', {
        'products': products
    })