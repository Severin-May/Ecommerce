from django.contrib import messages
from django.shortcuts import render, redirect
import datetime
from cart.cart import Cart
from django.template.context_processors import request
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from store.models import Product, Profile


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
        return render(request, 'payment/checkout.html', {"prods": prods, "quantities": quantities, "total": total, "shipping_form":ShippingForm(request.POST or None)})

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
            messages.error(request, "You are not logged in!!!")
            return render(request, 'payment/billing_info.html',
                          {"prods": prods, "quantities": quantities, "total": total, "shipping_details": request.POST, "billing_form": PaymentForm()})

    else:
        messages.error(request, "Access denied")
        return redirect('home')

def order_processing(request):
    if request.POST:
        cart = Cart(request)
        total = cart.total()
        prods = cart.get_products()
        quantities = cart.get_quantities()

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

            order_id = order_details.pk #primary_key

            for prod in prods:
                product_id = prod.id
                if prod.is_sale:
                    product_price = prod.sale_price
                else:
                    product_price = prod.price

                for key, value in quantities.items():
                    if int(key) == prod.id:
                        order_item_details = OrderItem(order_id=order_id, product_id=product_id, user=order_user, quantity=value, price=product_price)
                        order_item_details.save()

            for key in list(request.session.keys()):
                if key == 'session_key':
                    del request.session[key]

            curr_user = Profile.objects.filter(user__id=request.user.id)
            curr_user.update(old_cart="")

            messages.error(request, "Your order was placed!!!")
            return redirect('home')
        else:
            order_details = Order(full_name=order_fullname, email=order_email, address=ship_order_address, amount_paid=order_amount)
            order_details.save()
            order_id = order_details.pk  # primary_key

            for prod in prods:
                product_id = prod.id
                if prod.is_sale:
                    product_price = prod.sale_price
                else:
                    product_price = prod.price

                for key, value in quantities.items():
                    if int(key) == prod.id:
                        order_item_details = OrderItem(order_id=order_id, product_id=product_id, quantity=value, price=product_price)
                        order_item_details.save()

            for key in list(request.session.key()):
                if key == 'session_key':
                    del request.session[key]

            messages.error(request, "Your order was placed without logging in!!!")
            return redirect('home')
    else:
        messages.error(request, "Access denied!!!")
        return redirect('home')


def shipped_orders(request):

    if request.user.is_authenticated and request.user.is_superuser:
        shipped_orders = Order.objects.filter(is_shipped=True)

        if request.POST:
            status = request.POST['ship_status']
            num = request.POST['num']
            curr_order = Order.objects.filter(id=num)
            curr_order.update(is_shipped=False, date_shipped=datetime.datetime.now())

            messages.success(request, "Ship status has been changed!")
            return redirect('home')
        return render(request, 'payment/shipped_orders.html',{"shipped_orders":shipped_orders})
    else:
        messages.error(request, "Access denied!!!")
        return redirect('home')

def pending_orders(request):
    if request.user.is_authenticated and request.user.is_superuser:
        pending_orders = Order.objects.filter(is_shipped=False)
        if request.POST:
            status = request.POST['ship_status']
            num = request.POST['num']
            curr_order = Order.objects.filter(id=num)
            curr_order.update(is_shipped=True, date_shipped=datetime.datetime.now())

            messages.success(request, "Ship status has been changed!")
            return redirect('home')
        return render(request, 'payment/pending_orders.html',{"pending_orders":pending_orders})
    else:
        messages.error(request, "Access denied!!!")
        return redirect('home')

def orders(request, pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order = Order.objects.get(id=pk)
        order_items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['ship_status']
            if status == 'true':
                curr_order = Order.objects.filter(id=pk)
                curr_order.update(is_shipped=True, date_shipped=datetime.datetime.now())
            else:
                curr_order = Order.objects.filter(id=pk)
                curr_order.update(is_shipped=False)
            messages.success(request, "Ship status has been changed!")
            return redirect('home')
        return render(request, 'payment/orders.html',{"order":order, "order_items":order_items})
    else:
        messages.error(request, "Access denied!!!")
        return redirect('home')