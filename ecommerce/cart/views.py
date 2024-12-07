from itertools import product
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from .cart import Cart
from django.http import JsonResponse
from store.models import Product


# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    return render(request, 'cart_summary.html', {"prods": cart.get_products(), "quantities" : cart.get_quantities(), "total": cart.total()})

def cart_delete(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        id = int(request.POST.get('product_id'))
        cart.delete(product=id)
        messages.success(request, "Item was removed from the cart!")
        return JsonResponse({"quantity": id})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        id = int(request.POST.get('product_id'))
        qty = int(request.POST.get('product_quantity'))
        product = get_object_or_404(Product, id=id)
        cart.add(product=product, quantity=qty)
        response = JsonResponse({'Product Name: ': product.name, 'qty: ': cart.__len__()})
        messages.success(request, "Item was added to the cart!")
        return response

def cart_update(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        id = int(request.POST.get('product_id'))
        qty = str(request.POST.get('product_quantity'))

        cart.update(product=id, quantity=qty)

        messages.success(request, "Item quantity was changed!")
        return JsonResponse({"quantity": qty})