from django.http import JsonResponse
from django.shortcuts import render, redirect

from product.models import Product


# Create your views here.

def product_create(request):

    if request.method == "POST":
        Product.objects.create(
            name=request.POST['name'],
            barcode=request.POST['barcode'],
            sku=request.POST.get('sku'),
            purchase_price=request.POST.get('purchase_price') or 0,
            sale_price=request.POST.get('sale_price') or 0,
        )
        return redirect('dashboard')

    return render(request, 'product_add.html')



def product_list(request):
    products = Product.objects.all().order_by('-id')

    return render(request, 'product_list.html', {
        'products': products
    })