from django.conf import settings
from .models import Product, DiscountCode


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID, None)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {
                "total_price": 0,
                "discount_price": 0,
                "discount_code": None,
                "discount_percent": 0}
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
            "discount_price": self.cart['discount_price'],
            "discount_code": self.cart['discount_code'],
            "discount_percent": self.cart['discount_percent'],
        }
        return cart_info
    
    def set_discount_code(self, discount_code, discount_percent):
        self.cart['discount_code'] = discount_code
        print(discount_percent)
        self.cart['discount_percent'] = discount_percent
        self.save()
        self.cart['discount_price'] = self.cart["total_price"] / 100 * self.cart['discount_percent']
        print(self.cart)

    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.save()
    
    def clear(self):
        self.cart.clear()
        print(self.cart)
        self.save()