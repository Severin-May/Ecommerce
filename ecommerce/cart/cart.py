from store.models import Product

class Cart():
    def __init__(self, request):
        self.session = request.session

        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

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

    def __len__(self):
        return len(self.cart)

    def get_products(self):
        prod_ids = self.cart.keys()
        prods = Product.objects.filter(id__in=prod_ids)

        return prods

    def get_quantities(self):
        quantities = self.cart
        return quantities