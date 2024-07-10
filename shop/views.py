from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .models import Product, Category, DiscountCode, Order
from django.core.paginator import Paginator
from .Cart import Cart
from django.db.models import F
from datetime import datetime


class HomeView(View):
    template_name = "ecommerce/home.html"

    def get(self, request, *args, **kwargs):
        ordering = request.GET.get("order", None)
        if ordering == "new":
            order = "created"
        elif ordering == "old":
            order = "-created"
        elif ordering == "expensive":
            order = "price"
        elif ordering == "inexpensive":
            order = "-price"
        else:
            order = None
        # this database can not support Order_by, need to change db
        # if order:
        #     products_list = Product.objects.filter(available=True).order_by(order)
        # else:
        products_list = Product.objects.filter(available=True)
        
        paginator = Paginator(products_list, 5)
        current_page = request.GET.get('page', 1)
        page = paginator.get_page(current_page)
        context = {
            "products_list": page,
            "total_pages": paginator.num_pages,
            "total_products": paginator.count,
            'title_page': 'لیست محصولات ',
            'title': 'لیست همه محصولات ',
            }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class ProductDetailView(View):
    template_name = 'ecommerce/product_detail.html'

    def setup(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, id=pk)
        msg = "unavailable" if not product.available or product.quantity < 1 else "available"
        print(msg)
        cart = Cart(request)
        self.context = {
            "product": product,
            "product_id_cart": cart.check_product_in_cart(product.id),
            "cart_info": cart.cart_info(),
            "product_status": msg,
        }
        return super().setup(request, pk, *args, **kwargs)
    
    def get(self, request, pk, *args, **kwargs):
        return render(request, self.template_name, self.context)

    def post(self, request, pk, *args, **kwargs):
        return render(request, self.template_name, self.context)


class UpdateCartView(View):
    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        product_id = request.GET.get("product", None)
        product = get_object_or_404(Product, id=product_id, available=True, quantity__gte=1)
        product.quantity = F("quantity") - 1
        product.save()
        cart.add_or_remove(product)
        next = request.GET.get("next", None)
        if next:
            return redirect(next)
        else:
            return redirect("profile")


class CategoryView(View):
    template_name = "ecommerce/home.html"

    def get(self, request, slug, *args, **kwargs):
        category = get_object_or_404(Category, available=True, slug=slug)
        products_list = Product.objects.filter(category=category)
        paginator = Paginator(products_list, 20)
        current_page = request.GET.get("page", 1)
        page = paginator.get_page(current_page)
        context = {
            'products_list': page,
            'total_pages': paginator.num_pages,
            'total_products': paginator.count,
            'title_page': category.name,
            'title': f'لیست محصولات دسته بندی: {category.name}',
        }
        return render(request, self.template_name, context)

    def post(self, request, slug, *args, **kwargs):
        return render(request, self.template_name, {})


class CategorysListView(View):
    template_name = "ecommerce/categorys.html"

    def get(self, request, *args, **kwargs):
        categorys = Category.objects.filter(available=True)
        context = {
            'categorys_list': categorys
        }
        return render(request, self.template_name, context)


class CartUnRegisteredUserView(View):
    """For users that is not registered"""
    template_name = "ecommerce/cart-checkout.html"

    def setup(self, request, *args, **kwargs):
        self.cart = Cart(request)
        self.context = {
            "cart_info": self.cart.cart_info(),
        }
        return super().setup(request, *args, **kwargs)

    def get(self, request, *args, **kawrgs):
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kawrgs):
        discount_code = request.POST.get('discount_code', None)
        if discount_code:
            if not self.cart.cart['discount_code']:
                try:
                    discount = DiscountCode.objects.get(code=discount_code, available=True, current_use__lt=F("max_use"))
                    discount.current_use = F("current_use") + 1
                    discount.save()
                    self.cart.set_discount_code(discount.code, discount.percent)
                    msg = "success"
                except DiscountCode.DoesNotExist:
                    msg = "not found"
            else:
                msg = "last use"
            self.context.update({"msg": msg, "cart_info": self.cart.cart_info()})
        
        pay = request.POST.get('pay', "off")
        if pay == "on":
            cart = self.cart.cart_info()
            price = cart.get("total_price") - cart.get("discount_price")
            profile = request.user.profile
            if profile.coin >= price:
                profile.coin = F("coin") - price
                profile.save()
                self.cart.clear()
                if request.user.is_authenticated:
                    order = Order.objects.create(
                        user=request.user,
                        price=price
                    )
                    order.products.set([p for p in cart["products_list"]])
                    order.save()
                    return redirect("history")
                return redirect("home")
            else:
                self.context.update({"payment_msg": "not enough"})
        return render(request, self.template_name, self.context)