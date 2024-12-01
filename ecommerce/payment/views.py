from django.shortcuts import render

from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress


def payment_success(request):
    return render(request, "payment/payment_success.html", {})

def checkout(request):
    cart = Cart(request)
    prods = cart.get_products()
    quantities = cart.get_quantities()
    total = cart.total()

    if request.user.is_authenticated:
        shipping_user = ShippingAddress.objects.get(user=request.user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'payment/checkout.html', {"prods": prods, "quantities": quantities, "total": total, "shipping_form":shipping_form})
    else:
        shipping_form = ShippingForm(request.POST or None)
        return render(request, 'payment/checkout.html', {"prods": prods, "quantities": quantities, "total": total, "shipping_form":shipping_form})

