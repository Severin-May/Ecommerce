from django.template.context_processors import request
from store.models import Product, Profile


class Cart():
    def __init__(self, request):
        self.session = request.session
        self.request = request

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def total(self):
        ids = self.cart.keys()
        products = Product.objects.filter(id__in=ids)
        quantities = self.cart
        total = 0

        for key, value in quantities.items():
            key = int(key)
            for prod in products:
                if prod.id == key:
                    if prod.is_sale:
                        total += prod.sale_price * int(value)
                    else:
                        total += prod.price * int(value)
        return total

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        if self.request.user.is_authenticated:
            user = Profile.objects.filter(user__id=self.request.user.id)
            cart_str = str(self.cart)
            cart_str = cart_str.replace("\'", "\"")
            user.update(old_cart=str(cart_str))

    def update(self, product, quantity):
        id = str(product)
        quantity = str(quantity)

        cart = self.cart

        cart[id] = quantity

        self.session.modified = True

        if self.request.user.is_authenticated:
            user = Profile.objects.filter(user__id=self.request.user.id)
            cart_str = str(self.cart)
            cart_str = cart_str.replace("\'", "\"")
            user.update(old_cart=str(cart_str))

        return self.cart

    def add(self, product, quantity):
        id = str(product.id)
        quantity = str(quantity)

        if id in self.cart:
            pass
        else:
            self.cart[id] = int(quantity)

        self.session.modified = True

        if self.request.user.is_authenticated:
            user = Profile.objects.filter(user__id=self.request.user.id)
            cart_str = str(self.cart)
            cart_str = cart_str.replace("\'", "\"")
            user.update(old_cart=str(cart_str))


    def __len__(self):
        return len(self.cart)

    def get_products(self):
        return Product.objects.filter(id__in=self.cart.keys())

    def get_quantities(self):
        return self.cart

    def db_add(self, product, quantity):
        id = str(product)
        quantity = str(quantity)

        if id in self.cart:
            pass
        else:
            self.cart[id] = int(quantity)

        self.session.modified = True

        if self.request.user.is_authenticated:
            curr_user = Profile.objects.filter(user__id=self.request.user.id)
            cart_str = str(self.cart)
            cart_str = cart_str.replace("\'", "\"")
            curr_user.update(old_cart=str(cart_str))