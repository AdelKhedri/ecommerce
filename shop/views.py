from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from .models import Product
from django.core.paginator import Paginator


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
            "total_products": paginator.count
            }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class ProductDetailView(View):
    template_name = 'ecommerce/product_detail.html'

    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        context = {
            "product": product,
        }
        return render(request, self.template_name, context)

    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        context = {
            "product": product,
        }
        return render(request, self.template_name, context)