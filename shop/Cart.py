from django.conf import settings
from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID, None)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {"total_price": 0}
        self.cart = cart

    def add_or_remove(self, product):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'price': product.price}
            self.cart['total_price'] += product.price
        else:
            self.cart.pop(product_id)
            self.cart['total_price'] -= product.price
        self.save()

    def check_product_in_cart(self, product_id):
        return False if str(product_id) not in self.cart else True

    def cart_info(self):
        products_id_list = []
        for i, p in self.cart.items():
            if i.isnumeric():
                products_id_list.append(i)
        products_list = Product.objects.filter(id__in=products_id_list)
        cart_info = {
            "products_list": products_list,
            "total_price": self.cart.get('total_price', 0),
        }
        return cart_info

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.save()
    
    def clear(self):
        self.cart.clear()
        self.save()