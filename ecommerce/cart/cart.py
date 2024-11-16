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
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += product.sale_price * int(value)
                    else:
                        total += product.price * int(value)
        return total

    def delete(self, product):
        product_id = str(product)
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def update(self, product, quantity):
        product_id = str(product)
        product_quantity = str(quantity)

        cart = self.cart

        cart[product_id] = product_quantity

        self.session.modified = True

    def add(self, product, quantity):
        product_id = str(product.id)
        product_quantity = str(quantity)

        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price': str(product.price)}
            self.cart[product_id] = int(product_quantity)

        self.session.modified = True

        if self.request.user.is_authenticated:
            curr_user = Profile.objects.filter(user__id=self.request.user.id)
            cart_str = str(self.cart)
            cart_str = cart_str.replace("\'", "\"")
            curr_user.update(old_cart=str(cart_str))


    def __len__(self):
        return len(self.cart)

    def get_products(self):
        prod_ids = self.cart.keys()
        prods = Product.objects.filter(id__in=prod_ids)

        return prods

    def get_quantities(self):
        quantities = self.cart
        return quantities