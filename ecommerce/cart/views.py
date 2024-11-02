from django.shortcuts import render, get_object_or_404
from .cart import Cart
from django.http import JsonResponse

from store.models import Product


# Create your views here.
def cart_summary(request):
    cart = Cart(request)
    prods = cart.get_products()
    quantities = cart.get_quantities()
    return render(request, 'cart_summary.html', {"prods": prods, "quantities" : quantities})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))
        product = get_object_or_404(Product, id=product_id)
        cart.add(product=product, quantity=product_quantity)
        cart_quantity = cart.__len__()
        response = JsonResponse({'Product Name: ': product.name, 'qty: ': cart_quantity})

        return response

def cart_delete(request):
    pass

def cart_update(request):
    pass