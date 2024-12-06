from django.contrib import messages
from django.shortcuts import render, redirect

from cart.cart import Cart
from django.template.context_processors import request
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User


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

def billing_info(request):
    if request.POST:
        cart = Cart(request)
        prods = cart.get_products()
        quantities = cart.get_quantities()
        total = cart.total()

        shipping_details = request.POST
        request.session['shipping_details'] = shipping_details

        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, 'payment/billing_info.html',
                          {"prods": prods, "quantities": quantities, "total": total, "shipping_details": request.POST, "billing_form": billing_form})
        else:
            billing_form = PaymentForm()
            messages.error(request, "You are not logged in!!!")
            return render(request, 'payment/billing_info.html',
                          {"prods": prods, "quantities": quantities, "total": total, "shipping_details": request.POST, "billing_form": billing_form})

    else:
        messages.error(request, "Access denied")
        return redirect('home')

def process_order(request):
    if request.POST:
        cart = Cart(request)
        total = cart.total()

        payment_form = PaymentForm(request.POST or None)

        ship_details = request.session.get('shipping_details')
        ship_order_address = f"{ship_details['ship_address1']}\n{ship_details['ship_address2']}\n{ship_details['ship_city']}\n{ship_details['ship_state']}\n{ship_details['ship_country']}\n{ship_details['ship_zipcode']}"

        order_fullname = ship_details['ship_full_name']
        order_email = ship_details['ship_email']
        order_amount = total

        if request.user.is_authenticated:
            order_user = request.user
            order_details = Order(user=order_user, full_name=order_fullname, email=order_email, address=ship_order_address, amount_paid=order_amount)
            order_details.save()
            messages.error(request, "Your order was placed!!!")
            return redirect('home')
        else:
            order_details = Order(full_name=order_fullname, email=order_email, address=ship_order_address, amount_paid=order_amount)
            order_details.save()
            messages.error(request, "Your order was placed!!!")
            return redirect('home')
    else:
        messages.error(request, "Access denied!!!")
        return redirect('home')

