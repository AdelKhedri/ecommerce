from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View
from .models import Product, Category
from django.core.paginator import Paginator
from .Cart import Cart
from django.db.models import F


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
        product = get_object_or_404(Product, id=pk, available=True, quantity__gte=1)
        cart = Cart(request)
        self.context = {
            "product": product,
            "product_id_cart": cart.check_product_in_cart(product.id),
            "cart_info": cart.cart_info(),
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