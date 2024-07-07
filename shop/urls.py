from django.urls import path, re_path
from . import views


app_name = "shop"
urlpatterns = [
    path('product/details/<int:pk>/', views.ProductDetailView.as_view(), name="product-detail"),
    re_path('^update-cart', views.UpdateCartView.as_view(), name="update cart"),
]