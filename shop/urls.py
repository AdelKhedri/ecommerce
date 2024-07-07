from django.urls import path
from . import views


app_name = "shop"
urlpatterns = [
    path('product/details/<int:pk>/', views.ProductDetailView.as_view(), name="product-detail")
]